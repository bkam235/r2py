"""HTML comparator — structural DOM similarity (§7.3)."""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from html.parser import HTMLParser

from ...types import ComparatorResult, EffectClass

_PASS_THRESHOLD = 0.7

# Attributes to ignore during comparison (implementation-specific)
_IGNORE_ATTR_PREFIXES = ("data-require-", "data-bs-")
_IGNORE_ATTRS = frozenset({"bsOptions"})

# Wrapper tags to strip (page scaffolding)
_WRAPPER_TAGS = frozenset({"html", "head", "body", "!doctype"})

_WS_RE = re.compile(r"\s+")


class _DomNode:
    __slots__ = ("tag", "attrs", "children", "text")

    def __init__(self, tag: str = ""):
        self.tag = tag
        self.attrs: dict[str, str] = {}
        self.children: list[_DomNode] = []
        self.text: str = ""


class _DomParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = _DomNode("__root__")
        self._stack: list[_DomNode] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        node = _DomNode(tag.lower())
        node.attrs = {k: (v or "") for k, v in attrs}
        self._stack[-1].children.append(node)
        self._stack.append(node)

    def handle_endtag(self, tag: str):
        if len(self._stack) > 1:
            self._stack.pop()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]):
        node = _DomNode(tag.lower())
        node.attrs = {k: (v or "") for k, v in attrs}
        self._stack[-1].children.append(node)

    def handle_data(self, data: str):
        text = _WS_RE.sub(" ", data).strip()
        if text:
            node = _DomNode("")
            node.text = text
            self._stack[-1].children.append(node)


def _parse_html(html: str) -> _DomNode:
    parser = _DomParser()
    parser.feed(html)
    return parser.root


def _unwrap(node: _DomNode) -> _DomNode:
    """Strip html/head/body wrappers to get to content nodes."""
    if node.tag == "__root__" and len(node.children) == 1:
        child = node.children[0]
        if child.tag in _WRAPPER_TAGS:
            return _unwrap(child)
    if node.tag in _WRAPPER_TAGS:
        # Find body or return the node's children as a new root
        for child in node.children:
            if child.tag == "body":
                wrapper = _DomNode("__root__")
                wrapper.children = child.children
                return wrapper
        wrapper = _DomNode("__root__")
        wrapper.children = [c for c in node.children if c.tag not in _WRAPPER_TAGS]
        return wrapper
    return node


def _filter_attrs(attrs: dict[str, str]) -> dict[str, str]:
    """Keep only semantically meaningful attributes."""
    result = {}
    for k, v in attrs.items():
        if k in _IGNORE_ATTRS:
            continue
        if any(k.startswith(p) for p in _IGNORE_ATTR_PREFIXES):
            continue
        result[k] = v
    return result


def _tokenize(node: _DomNode) -> list[str]:
    """Flatten DOM tree into a sequence of structural tokens."""
    tokens: list[str] = []
    _tokenize_recursive(node, tokens)
    return tokens


def _tokenize_recursive(node: _DomNode, tokens: list[str]):
    if node.text:
        tokens.append(f"T:{node.text}")
        return

    if node.tag and node.tag != "__root__":
        attrs = _filter_attrs(node.attrs)
        # Include class and id in the tag token (most semantic attrs)
        parts = [node.tag]
        if "class" in attrs:
            classes = sorted(attrs["class"].split())
            parts.append(f'.{".".join(classes)}')
        if "id" in attrs:
            parts.append(f"#{attrs['id']}")
        if "type" in attrs:
            parts.append(f"[type={attrs['type']}]")
        tokens.append(f"<{' '.join(parts)}>")

    for child in node.children:
        _tokenize_recursive(child, tokens)

    if node.tag and node.tag != "__root__":
        tokens.append(f"</{node.tag}>")


def _dom_similarity(html_r: str, html_py: str) -> float:
    """Compare two HTML strings structurally using tokenized DOM sequences."""
    tree_r = _unwrap(_parse_html(html_r))
    tree_py = _unwrap(_parse_html(html_py))

    tokens_r = _tokenize(tree_r)
    tokens_py = _tokenize(tree_py)

    if not tokens_r and not tokens_py:
        return 1.0
    if not tokens_r or not tokens_py:
        return 0.0

    return SequenceMatcher(None, tokens_r, tokens_py).ratio()


def _best_match_score(r_items: list[str], py_items: list[str]) -> float:
    """Score HTML lists using best-match pairing (greedy).

    For each R item, find the Python item with the highest DOM similarity.
    Score = average of matched R items. Extra Python items are not penalized
    (they're noise, not errors — the translation still produces correct output).
    Missing Python items (fewer than R) score 0 for that slot.
    """
    n_r, n_py = len(r_items), len(py_items)
    if n_r == 1 and n_py == 1:
        return _dom_similarity(r_items[0], py_items[0])

    # Compute full similarity matrix
    matrix = [
        [_dom_similarity(r_items[i], py_items[j]) for j in range(n_py)]
        for i in range(n_r)
    ]

    # Greedy best-match: assign each R item to its best available Python item
    used_py: set[int] = set()
    matched_scores: list[float] = []
    r_order = sorted(range(n_r), key=lambda i: max(matrix[i]), reverse=True)
    for i in r_order:
        best_j = -1
        best_s = -1.0
        for j in range(n_py):
            if j not in used_py and matrix[i][j] > best_s:
                best_s = matrix[i][j]
                best_j = j
        if best_j >= 0:
            used_py.add(best_j)
            matched_scores.append(best_s)
        else:
            matched_scores.append(0.0)

    # Average over R item count (how well is R's output covered?)
    return sum(matched_scores) / n_r


class HtmlComparator:
    effect_class = EffectClass.HTML

    def compare(self, r_effect: list[str], py_effect: list[str]) -> ComparatorResult:
        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.HTML, score=1.0, verdict="pass")

        if not r_effect or not py_effect:
            return ComparatorResult(
                effect_class=EffectClass.HTML,
                score=0.0,
                verdict="fail",
                explanation=f"HTML present on one side only: R={len(r_effect)} Python={len(py_effect)}",
                failure_tag="value",
            )

        # Best-match pairing: for each R item find the best-matching Python item.
        # Unmatched extras on either side get a small penalty rather than 0.
        score = _best_match_score(r_effect, py_effect)
        verdict = "pass" if score >= _PASS_THRESHOLD else "fail"
        if verdict == "pass":
            explanation = f"html_content_compared:{len(r_effect)}"
        else:
            explanation = f"HTML DOM similarity {score:.3f} < {_PASS_THRESHOLD}"
        return ComparatorResult(
            effect_class=EffectClass.HTML,
            score=score,
            verdict=verdict,
            explanation=explanation,
        )
