"""Graphics comparator — byte-exact then pixel RMSE (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass

_PASS_THRESHOLD = 0.9


def _pillow_rmse(r_bytes: bytes, py_bytes: bytes) -> float | None:
    """Return normalized RMSE in [0, 1] (0 = identical) or None if Pillow absent."""
    try:
        from PIL import Image  # type: ignore[import]
        import io
        import math

        r_img = Image.open(io.BytesIO(r_bytes)).convert("L")
        py_img = Image.open(io.BytesIO(py_bytes)).convert("L")
        if r_img.size != py_img.size:
            py_img = py_img.resize(r_img.size, Image.LANCZOS)
        r_px = list(r_img.getdata())
        py_px = list(py_img.getdata())
        mse = sum((a - b) ** 2 for a, b in zip(r_px, py_px)) / len(r_px)
        return math.sqrt(mse) / 255.0
    except Exception:
        return None


class GraphicsComparator:
    effect_class = EffectClass.GRAPHICS

    def compare(self, r_effect: list[bytes], py_effect: list[bytes]) -> ComparatorResult:
        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.GRAPHICS, score=1.0, verdict="pass")

        if len(r_effect) != len(py_effect):
            return ComparatorResult(
                effect_class=EffectClass.GRAPHICS,
                score=0.0,
                verdict="fail",
                explanation=f"figure count differs: R={len(r_effect)} Python={len(py_effect)}",
                failure_tag="value",
            )

        scores: list[float] = []
        for r_bytes, py_bytes in zip(r_effect, py_effect):
            if r_bytes == py_bytes:
                scores.append(1.0)
                continue
            rmse = _pillow_rmse(r_bytes, py_bytes)
            if rmse is None:
                return ComparatorResult(
                    effect_class=EffectClass.GRAPHICS,
                    score=0.0,
                    verdict="uncomparable",
                    explanation="Pillow not available; cannot compare non-identical graphics",
                )
            scores.append(max(0.0, 1.0 - rmse))

        score = sum(scores) / len(scores)
        verdict = "pass" if score >= _PASS_THRESHOLD else "fail"
        explanation = "" if verdict == "pass" else f"graphics similarity {score:.3f} < {_PASS_THRESHOLD}"
        return ComparatorResult(
            effect_class=EffectClass.GRAPHICS,
            score=score,
            verdict=verdict,
            explanation=explanation,
            failure_tag="value" if verdict == "fail" else None,
        )
