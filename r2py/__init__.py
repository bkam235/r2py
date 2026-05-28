"""r2py v0.2 — R-to-Python execution-verified translator."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import ScriptMap, TranslateResult

__version__ = "0.2.0"
__all__ = ["translate", "analyze"]


def translate(
    r_path: "str | Path",
    py_path: "str | Path",
    *,
    max_iters: int = 8,
    score_threshold: float = 0.85,
    beam_width: int = 4,
    use_judge: bool = False,          # D4: LLM judge off by default
    learned_retrieval: bool = False,  # D6: learned reranker off by default
    learned_policy: bool = False,     # D6: learned edit policy off by default
    data_compare: str = "auto",       # "auto" | "exact" | "embedding"
    sandbox: str = "subprocess",
    no_seeds: bool = False,           # ignore seed:true patterns (§6.7 transfer experiment)
) -> "TranslateResult":
    """Translate an R script to Python.

    Wired to the beam-search loop in step 7 of the implementation order,
    after Stages 0–4 and the Pattern Library are built.
    """
    raise NotImplementedError(
        "translate() requires Stages 0–4 and the beam-search loop (architecture step 7)"
    )


def analyze(r_path: "str | Path") -> "ScriptMap":
    """Analyze an R script and return its ScriptMap (architecture step 2, Stage 1)."""
    raise NotImplementedError(
        "analyze() requires Stage 1 (architecture step 2)"
    )
