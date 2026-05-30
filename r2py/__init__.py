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
    library=None,                    # inject a PatternLibrary (or _FrozenLibrary); None → get_library()
    model: "str | None" = None,  # Anthropic model ID, or "ollama:<name>" for local Ollama; None → _DEFAULT_MODEL
    max_iters: int = 8,
    score_threshold: float = 0.85,
    beam_width: int = 4,
    use_judge: bool = False,         # D4: LLM judge off by default
    learned_retrieval: bool = False, # D6: learned reranker (§12.6 A); off by default
    learned_policy: bool = False,    # D6: learned edit policy (§12.6 B); off by default
    data_compare: str = "auto",      # "auto" | "exact" | "embedding"
    sandbox: str = "subprocess",
    no_seeds: bool = False,          # ignore seed:true patterns (§6.7 transfer experiment)
    output_dir: "str | Path | None" = None,  # if set, write edits.log.jsonl + library_diff.json
) -> "TranslateResult":
    """Translate an R script to Python via the beam/strict-improvement loop (§4.1)."""
    from pathlib import Path
    from .stage1 import analyze as _analyze
    from .library import get_library
    from .loop import run_loop
    from .stage2.llm import _DEFAULT_MODEL
    if model is None:
        model = _DEFAULT_MODEL

    if library is None:
        library = get_library()

    result = run_loop(
        _analyze(Path(r_path)),
        library,
        max_iters=max_iters,
        score_threshold=score_threshold,
        beam_width=beam_width,
        use_judge=use_judge,
        data_compare=data_compare,
        no_seeds=no_seeds,
        learned_retrieval=learned_retrieval,
        learned_policy=learned_policy,
        output_dir=Path(output_dir) if output_dir is not None else None,
        model=model,
    )
    Path(py_path).write_text(result.python_source, encoding="utf-8")
    return result


def analyze(r_path: "str | Path") -> "ScriptMap":
    """Analyze an R script and return its ScriptMap (§3)."""
    from pathlib import Path
    from .stage1 import analyze as _analyze
    return _analyze(Path(r_path))
