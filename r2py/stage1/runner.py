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


def run_script_checkpointed(
    r_source: str,
    entities: dict,
    capture: CaptureSpec = DEFAULT_CAPTURE,
    timeout_s: float = 60,
) -> "tuple[EffectBundle, dict[str, EffectBundle]]":
    """Run R source with per-entity checkpoint captures.

    Injects a `.r2py_cp(eid)` call after each entity's last source line.
    The checkpoint function serializes new namespace variables (and graphics count
    delta) to ``_r2py_cp_{eid}.json`` files in the workdir during a single R run.

    Returns ``(full_bundle, entity_bundles)`` where ``entity_bundles`` maps
    entity_id → per-entity EffectBundle delta.  Falls back silently: if
    jsonlite is unavailable or the R run fails, ``entity_bundles`` is empty
    and ``full_bundle`` is the normal whole-script bundle.
    """
    import json as _json

    from ..stage0.sandbox.r_sandbox import RSandbox
    from ..stage0.sandbox.isolation import TempWorkdir
    from ..stage0.effects import bundle as _bundle_mod

    # Build sorted list of (end_line_0based, entity_id) pairs.
    entity_boundaries: list[tuple[int, str]] = []
    for eid, entity in entities.items():
        sp = getattr(entity, "source_span", None)
        if sp is not None:
            entity_boundaries.append((sp.end_line, eid))
    # Sort ascending so we can inject bottom-up (preserves earlier line numbers).
    entity_boundaries.sort(key=lambda x: x[0])

    # Build checkpoint preamble (R).
    r_cp_preamble = _R_CHECKPOINT_PREAMBLE

    # Inject `.r2py_cp("eid")` after each entity's last line (bottom-up to keep
    # line numbers stable for earlier insertions).
    lines = r_source.splitlines(keepends=True)
    # Bottom-up: process in reverse end_line order.
    for end_line_0, eid in reversed(entity_boundaries):
        insert_after = min(end_line_0, len(lines) - 1)
        safe_eid = eid.replace('"', '\\"').replace("\\", "\\\\")
        checkpoint_line = f'\n.r2py_cp("{safe_eid}")\n'
        lines.insert(insert_after + 1, checkpoint_line)

    checkpointed_source = "".join(lines)

    with TempWorkdir() as workdir:
        sandbox = RSandbox()
        try:
            full_bundle = sandbox.run(
                checkpointed_source,
                workdir=workdir,
                capture=capture,
                preamble=r_cp_preamble,
                timeout_s=timeout_s,
            )
        except Exception:
            # If the checkpointed run fails, fall back to plain run.
            full_bundle = sandbox.run(
                r_source,
                workdir=workdir,
                capture=capture,
                timeout_s=timeout_s,
            )
            return full_bundle, {}

        # Parse per-entity checkpoint files.
        entity_bundles: dict[str, EffectBundle] = {}
        for _, eid in entity_boundaries:
            safe_eid = eid.replace("/", "_").replace(":", "_")
            cp_path = workdir / f"_r2py_cp_{safe_eid}.json"
            if not cp_path.exists():
                continue
            try:
                cp_data = _json.loads(cp_path.read_text(encoding="utf-8"))
                raw_data = cp_data.get("data", {})
                # jsonlite serialises an empty R list() as [] not {}; normalise.
                if not isinstance(raw_data, dict):
                    raw_data = {}
                eb = EffectBundle(
                    data=raw_data,
                    stdout=cp_data.get("stdout", ""),
                    graphics=cp_data.get("graphics", 0),
                )
                entity_bundles[eid] = eb
            except Exception:
                continue

        return full_bundle, entity_bundles


# R preamble that defines the checkpoint function used by run_script_checkpointed.
_R_CHECKPOINT_PREAMBLE = r"""
.r2py_prev_vars <- character(0)
.r2py_prev_fig_count <- 0L
.r2py_stdout_buf <- character(0)
.r2py_prev_stdout_len <- 0L

# Redirect stdout into a text connection so we can capture per-entity deltas.
.r2py_stdout_con <- textConnection(".r2py_stdout_buf", open = "w", local = FALSE)
sink(.r2py_stdout_con, type = "output", append = FALSE)

.r2py_cp <- function(eid) {
  tryCatch({
    cur_vars <- setdiff(
      ls(envir = .GlobalEnv),
      c(".r2py_prev_vars", ".r2py_prev_fig_count", ".r2py_cp",
        ".r2py_stdout_buf", ".r2py_stdout_con", ".r2py_prev_stdout_len")
    )
    new_vars <- setdiff(cur_vars, .r2py_prev_vars)
    state <- list()
    for (v in new_vars) {
      obj <- get(v, envir = .GlobalEnv)
      if (!is.function(obj) && !is.environment(obj)) {
        state[[v]] <- obj
      }
    }
    cur_fig_count <- length(grDevices::dev.list())
    graphics_delta <- max(0L, cur_fig_count - .r2py_prev_fig_count)

    # Flush sink so .r2py_stdout_buf is up to date, then compute delta.
    sink(type = "output")
    sink(.r2py_stdout_con, type = "output", append = TRUE)
    cur_len <- length(.r2py_stdout_buf)
    stdout_lines <- if (cur_len > .r2py_prev_stdout_len)
      .r2py_stdout_buf[(.r2py_prev_stdout_len + 1L):cur_len]
    else
      character(0)
    stdout_delta <- if (length(stdout_lines) > 0L)
      paste(stdout_lines, collapse = "\n")
    else
      ""

    cp <- list(
      data = state,
      graphics = graphics_delta,
      stdout = stdout_delta
    )
    safe_eid <- gsub("[/:]", "_", eid)
    if (requireNamespace("jsonlite", quietly = TRUE)) {
      jsonlite::write_json(
        cp,
        paste0("_r2py_cp_", safe_eid, ".json"),
        auto_unbox = TRUE, null = "null", na = "null"
      )
    }
    .r2py_prev_vars <<- cur_vars
    .r2py_prev_fig_count <<- cur_fig_count
    .r2py_prev_stdout_len <<- cur_len
  }, error = function(e) invisible(NULL))
}
"""


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
