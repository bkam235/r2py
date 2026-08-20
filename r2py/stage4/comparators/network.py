"""Network side-effect comparator (§7.3)."""
from __future__ import annotations

from urllib.parse import urlparse

from ...types import ComparatorResult, EffectClass


def _normalize_url(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}{p.path}".rstrip("/").lower()


class NetworkComparator:
    effect_class = EffectClass.NETWORK

    def compare(self, r_effect: list[tuple], py_effect: list[tuple]) -> ComparatorResult:
        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.NETWORK, score=1.0, verdict="pass")

        r_set = {(verb, _normalize_url(target)) for verb, target, *_ in r_effect}
        py_set = {(verb, _normalize_url(target)) for verb, target, *_ in py_effect}

        if not r_set and not py_set:
            return ComparatorResult(effect_class=EffectClass.NETWORK, score=1.0, verdict="pass")

        intersection = r_set & py_set
        union = r_set | py_set
        score = len(intersection) / len(union) if union else 1.0

        verdict = "pass" if score >= 0.95 else "fail"
        explanation = ""
        if verdict == "fail":
            only_r = r_set - py_set
            only_py = py_set - r_set
            parts = []
            if only_r:
                parts.append(f"R-only requests: {sorted(only_r)}")
            if only_py:
                parts.append(f"Python-only requests: {sorted(only_py)}")
            explanation = "; ".join(parts)

        return ComparatorResult(
            effect_class=EffectClass.NETWORK,
            score=score,
            verdict=verdict,
            explanation=explanation,
            failure_tag="value" if verdict == "fail" else None,
        )
