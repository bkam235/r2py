"""Pattern dataclass and markdown (de)serialization (§6.2)."""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from datetime import date
from typing import Literal


Confidence = Literal["confirmed", "tentative", "contradicted"]

_VALID_CONFIDENCE = {"confirmed", "tentative", "contradicted"}


@dataclass
class EvidenceEntry:
    script_id:         str
    score:             float
    verification_path: str   # "exact" | "embedding" | "stdout" | "judge"
    variable:          str


@dataclass
class TranslationExample:
    """A verified (R snippet → Python snippet) pair attached to a Pattern."""
    r_hash:     str    # sha256[:8] of r_snippet — dedup key
    r_snippet:  str    # R source, capped at 300 chars
    py_snippet: str    # verified Python, capped at 600 chars
    score:      float  # entity score when recorded
    script_id:  str


@dataclass
class EditExample:
    """A verified before→after edit pair, keyed by the failure class it fixed."""
    failure_class: str    # EffectClass.value of the dominant failure at edit time
    old_code:      str    # before snippet, capped at 300 chars
    new_code:      str    # after snippet, capped at 300 chars
    score_delta:   float
    script_id:     str


def r_snippet_hash(r_snippet: str) -> str:
    """Return an 8-char hex hash of an R snippet — used as a dedup key."""
    return hashlib.sha256(r_snippet.encode()).hexdigest()[:8]


@dataclass
class Pattern:
    id:             str
    package:        str
    confidence:     Confidence
    seed:           bool
    guidance:       str
    evidence:       list[EvidenceEntry] = field(default_factory=list)
    contradictions: list[str]           = field(default_factory=list)
    created:        str                 = ""   # ISO date string
    last_review:    str                 = ""   # ISO date string
    # Counts of tie interactions (score == 0, no regression). Stored separately
    # from evidence so they don't inflate the demotion threshold. Old-format
    # files that stored ties as EvidenceEntry(verification_path="tie") are
    # migrated to this counter on deserialization.
    tie_count:             int                      = 0
    # Verified code examples (§plan: entity-level examples).
    # translation_examples: up to 3 (R→Python) pairs for Stage 2 bootstrapping.
    # edit_examples: up to 5 per failure_class for Stage 3 exploit mode.
    translation_examples:  list[TranslationExample] = field(default_factory=list)
    edit_examples:         list[EditExample]         = field(default_factory=list)

    # ------------------------------------------------------------------ #
    # Convenience                                                          #
    # ------------------------------------------------------------------ #

    def demotion_threshold(self) -> int:
        """Contradictions needed to trigger a demotion (§6.5).

        Scales only with genuine improvement evidence (score > 0). Tie entries
        are tracked separately in tie_count and do not raise the threshold —
        a pattern protected only by repeated tie interactions is no more
        established than one with no interactions at all.

        Seeds with no evidence use a minimum of 3 (same as patterns with some
        evidence) so a single bad application doesn't immediately kill a
        human-verified seed pattern.
        """
        real = sum(1 for e in self.evidence if e.score > 0.0)
        if real:
            return max(3, math.ceil(real * 0.75))
        return 5 if self.seed else 1


# ------------------------------------------------------------------ #
# Serialization helpers                                               #
# ------------------------------------------------------------------ #

_FRONT_MATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL
)
_EVIDENCE_LINE_RE = re.compile(
    r"^-\s+(.+?)\s+→\s+score\s+([\d.]+)\s+\(path:\s*([^,]+),\s*variable:\s*(.+?)\)\s*$"
)


def to_markdown(p: Pattern) -> str:
    """Serialize a Pattern to the §6.2 markdown front-matter format."""
    lines = [
        "---",
        f"id: {p.id}",
        f"package: {p.package}",
        f"confidence: {p.confidence}",
        f"seed: {'true' if p.seed else 'false'}",
        f"created: {p.created or date.today().isoformat()}",
        f"last_review: {p.last_review or date.today().isoformat()}",
        f"tie_count: {p.tie_count}",
        "---",
        "",
        f"# {p.id}",
        "",
        "## Guidance",
        p.guidance.strip(),
        "",
        "## Evidence",
    ]
    if p.evidence:
        for e in p.evidence:
            lines.append(
                f"- {e.script_id} → score {e.score:.3f}"
                f" (path: {e.verification_path}, variable: {e.variable})"
            )
    else:
        lines.append("(none)")
    lines += ["", "## Contradictions"]
    if p.contradictions:
        for c in p.contradictions:
            lines.append(f"- {c}")
    else:
        lines.append("(none)")
    lines += ["", "## Translation Examples"]
    if p.translation_examples:
        for ex in p.translation_examples:
            lines.append("- " + json.dumps({
                "r_hash": ex.r_hash, "r_snippet": ex.r_snippet,
                "py_snippet": ex.py_snippet, "score": round(ex.score, 4),
                "script_id": ex.script_id,
            }, ensure_ascii=False))
    else:
        lines.append("(none)")
    lines += ["", "## Edit Examples"]
    if p.edit_examples:
        for ex in p.edit_examples:
            lines.append("- " + json.dumps({
                "failure_class": ex.failure_class, "old_code": ex.old_code,
                "new_code": ex.new_code, "score_delta": round(ex.score_delta, 4),
                "script_id": ex.script_id,
            }, ensure_ascii=False))
    else:
        lines.append("(none)")
    lines.append("")
    return "\n".join(lines)


def from_markdown(text: str) -> Pattern:
    """Deserialize a Pattern from the §6.2 markdown front-matter format."""
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        raise ValueError("Missing front-matter block (--- ... ---)")
    front, body = m.group(1), m.group(2)

    meta: dict[str, str] = {}
    for line in front.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()

    pid        = meta.get("id", "")
    package    = meta.get("package", "")
    confidence = meta.get("confidence", "tentative")
    if confidence not in _VALID_CONFIDENCE:
        confidence = "tentative"
    seed       = meta.get("seed", "false").lower() == "true"
    created    = meta.get("created", "")
    last_review = meta.get("last_review", "")
    try:
        tie_count = int(meta.get("tie_count", "0"))
    except ValueError:
        tie_count = 0

    guidance, evidence, contradictions, translation_examples, edit_examples = _parse_body(body)

    # Migration: old files stored tie interactions as EvidenceEntry with
    # verification_path="tie". Move them to tie_count and strip from evidence.
    legacy_ties = sum(1 for e in evidence if e.verification_path == "tie")
    if legacy_ties:
        tie_count += legacy_ties
        evidence = [e for e in evidence if e.verification_path != "tie"]

    return Pattern(
        id=pid,
        package=package,
        confidence=confidence,  # type: ignore[arg-type]
        seed=seed,
        guidance=guidance,
        evidence=evidence,
        contradictions=contradictions,
        created=created,
        last_review=last_review,
        tie_count=tie_count,
        translation_examples=translation_examples,
        edit_examples=edit_examples,
    )


def _parse_body(
    body: str,
) -> tuple[str, list[EvidenceEntry], list[str], list[TranslationExample], list[EditExample]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    guidance = "\n".join(sections.get("Guidance", [])).strip()

    evidence: list[EvidenceEntry] = []
    for line in sections.get("Evidence", []):
        line = line.strip()
        if not line or line == "(none)":
            continue
        em = _EVIDENCE_LINE_RE.match(line)
        if em:
            evidence.append(EvidenceEntry(
                script_id=em.group(1),
                score=float(em.group(2)),
                verification_path=em.group(3).strip(),
                variable=em.group(4).strip(),
            ))

    contradictions: list[str] = []
    for line in sections.get("Contradictions", []):
        line = line.strip()
        if not line or line == "(none)":
            continue
        if line.startswith("- "):
            contradictions.append(line[2:])
        else:
            contradictions.append(line)

    translation_examples: list[TranslationExample] = []
    for line in sections.get("Translation Examples", []):
        line = line.strip()
        if not line or line == "(none)":
            continue
        if line.startswith("- "):
            line = line[2:]
        try:
            d = json.loads(line)
            translation_examples.append(TranslationExample(
                r_hash=d.get("r_hash", ""),
                r_snippet=d.get("r_snippet", ""),
                py_snippet=d.get("py_snippet", ""),
                score=float(d.get("score", 0.0)),
                script_id=d.get("script_id", ""),
            ))
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    edit_examples: list[EditExample] = []
    for line in sections.get("Edit Examples", []):
        line = line.strip()
        if not line or line == "(none)":
            continue
        if line.startswith("- "):
            line = line[2:]
        try:
            d = json.loads(line)
            edit_examples.append(EditExample(
                failure_class=d.get("failure_class", ""),
                old_code=d.get("old_code", ""),
                new_code=d.get("new_code", ""),
                score_delta=float(d.get("score_delta", 0.0)),
                script_id=d.get("script_id", ""),
            ))
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    return guidance, evidence, contradictions, translation_examples, edit_examples
