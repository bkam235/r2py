"""Pre-translation construct catalog — R-semantic flag guidance for LLM prompts."""
from __future__ import annotations

R_SEMANTIC_GUIDANCE: dict[str, str] = {
    "indexing_1based": (
        "R uses 1-based indexing; Python uses 0-based. Subtract 1 from all "
        "numeric subscripts (e.g., x[1] -> x[0]). R's x[1:3] returns 3 "
        "elements (inclusive end); translate to x[0:3] (exclusive end) in Python."
    ),
    "super_assign": (
        "R's <<- modifies a variable in the parent (enclosing) scope. Use "
        "'nonlocal' inside nested functions or 'global' at module level."
    ),
    "na_semantics": (
        "R's NA propagates through arithmetic and comparisons (NA + 1 = NA). "
        "Use numpy.nan or pandas.NA for data. Translate is.na(x) to "
        "pandas.isna(x), and na.rm=TRUE to skipna=True or the nanXxx variant "
        "(e.g., numpy.nanmean)."
    ),
    "nse": (
        "R uses non-standard evaluation (NSE): functions like filter(), "
        "select(), mutate(), aes(), and formula (~) capture unevaluated "
        "expressions. In Python equivalents (pandas, plotnine), pass column "
        "names as strings — never bare Python variable names."
    ),
    "vector_recycling": (
        "R silently recycles shorter vectors in binary operations to match "
        "the longer one. Python/numpy raise a shape mismatch error. Use "
        "numpy.resize() or numpy.tile() to match lengths explicitly."
    ),
    "copy_on_modify": (
        "R has copy-on-modify: b <- a makes an independent copy. Python "
        "assignment creates a reference. Use .copy() for lists, dict.copy() "
        "for dicts, or df.copy() for DataFrames to preserve R's behavior."
    ),
    "platform_specific": (
        "This code uses platform-specific R functions (Sys.setlocale, system, "
        "proc.time). Use Python's os, locale, subprocess, or time modules."
    ),
    "dispatch_s3s4r6": (
        "This code uses R's S3/S4/R6 dispatch (UseMethod, setGeneric, "
        "R6Class). Translate S3 generics to isinstance dispatch or class "
        "methods. R6Class becomes a Python class with __init__ and methods."
    ),
    "scalar_vs_vector": (
        "R has no scalar type — length(42) is 1. Translate length(x) to "
        "len(x). Be aware that a single R numeric becomes a Python scalar, "
        "not a length-1 list; wrap in a list if the code depends on R's "
        "'everything is a vector' semantics."
    ),
    "vector_constructor": (
        "R functions like complex(n), logical(n), integer(n) with a single "
        "argument create a zero-filled vector of length n — NOT a type "
        "conversion. Translate to numpy.zeros(n, dtype=...) or [default]*n."
    ),
}


def format_construct_notes(entities: dict) -> str:
    """Build a construct-catalog prompt section from flags present in entities.

    Returns empty string if no relevant flags are present.
    """
    seen_flags: set[str] = set()
    for entity in entities.values():
        for flag in getattr(entity, "r_semantic_flags", []):
            if not flag.startswith("python_keyword_arg:"):
                seen_flags.add(flag)

    if not seen_flags:
        return ""

    parts: list[str] = []
    for flag, guidance in R_SEMANTIC_GUIDANCE.items():
        if flag in seen_flags:
            parts.append(f"- **{flag}**: {guidance}")

    return "\n".join(parts)
