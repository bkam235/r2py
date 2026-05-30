"""Bridge from Stage 1 to Stage 0 sandboxes (§3.4 steps 2–3)."""
from __future__ import annotations

import re as _re
from pathlib import Path

# Valid bare R identifier: starts with letter or dot, contains only [A-Za-z0-9._]
_R_IDENT_RE = _re.compile(r"^[a-zA-Z.][a-zA-Z0-9._]*$")

from ..types import CaptureSpec, EffectBundle, EffectClass

# Default capture spec used for full script runs.
DEFAULT_CAPTURE: CaptureSpec = frozenset({
    EffectClass.STDOUT,
    EffectClass.FILES,
    EffectClass.GRAPHICS,
    EffectClass.DATA,
    EffectClass.ENV,
    EffectClass.WARNINGS,
})


def run_script(
    r_path: Path,
    capture: CaptureSpec = DEFAULT_CAPTURE,
    timeout_s: float = 60,
) -> EffectBundle:
    """Execute an R script and return its EffectBundle."""
    from ..stage0.sandbox.r_sandbox import RSandbox
    from ..stage0.sandbox.isolation import TempWorkdir

    source = r_path.read_text(encoding="utf-8")
    with TempWorkdir() as workdir:
        sandbox = RSandbox()
        return sandbox.run(
            source,
            workdir=workdir,
            capture=capture,
            timeout_s=timeout_s,
        )


def run_slice(
    r_source: str,
    capture: CaptureSpec = DEFAULT_CAPTURE,
    parent_state: dict | None = None,
    timeout_s: float = 30,
) -> EffectBundle:
    """Run an R source fragment, optionally restoring parent scope variables.

    *parent_state* maps variable names to Python values (from EffectBundle.data).
    Each entry is emitted as an R assignment preamble before the source is run.
    """
    from ..stage0.sandbox.r_sandbox import RSandbox
    from ..stage0.sandbox.isolation import TempWorkdir

    preamble = _build_preamble(parent_state or {})
    with TempWorkdir() as workdir:
        sandbox = RSandbox()
        return sandbox.run(
            r_source,
            workdir=workdir,
            capture=capture,
            preamble=preamble,
            timeout_s=timeout_s,
        )


def _build_preamble(state: dict) -> str:
    """Emit R assignment statements that restore *state* into the environment."""
    lines: list[str] = []
    for name, value in state.items():
        r_val = _py_to_r(value)
        if r_val is not None:
            lines.append(f"{name} <- {r_val}")
    return "\n".join(lines)


def _py_to_r(value: object) -> str | None:
    """Convert a Python value (from EffectBundle.data) to an R literal string.

    Returns None when the value cannot be represented as a simple literal.
    """
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, int):
        return f"{value}L"
    if isinstance(value, float):
        import math
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Inf" if value > 0 else "-Inf"
        return repr(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    if isinstance(value, list):
        parts = [_py_to_r(v) for v in value]
        if any(p is None for p in parts):
            return None
        if len(parts) == 1:
            return parts[0]
        return f"c({', '.join(parts)})"
    if isinstance(value, dict):
        items = []
        for k, v in value.items():
            rv = _py_to_r(v)
            if rv is None:
                return None  # give up if any nested value is too complex
            # Backtick-quote keys that are not valid bare R identifiers.
            raw_key = str(k)
            if _R_IDENT_RE.match(raw_key):
                safe_key = raw_key
            else:
                safe_key = "`" + raw_key.replace("\\", "\\\\").replace("`", "\\`") + "`"
            items.append(f"{safe_key}={rv}")
        return f"list({', '.join(items)})" if items else "list()"
    try:
        import pandas as _pd  # type: ignore
        if isinstance(value, _pd.DataFrame):
            j = value.to_json(orient="records")
            escaped = j.replace("\\", "\\\\").replace("'", "\\'")
            return f"jsonlite::fromJSON('{escaped}')"
    except ImportError:
        pass
    return None
