"""Bridge from Stage 1 to Stage 0 sandboxes (§3.4 steps 2–3)."""
from __future__ import annotations

import re as _re
from pathlib import Path

# Valid bare R identifier: starts with letter or dot, contains only [A-Za-z0-9._]
_R_IDENT_RE = _re.compile(r"^[a-zA-Z.][a-zA-Z0-9._]*$")
_CRAWLER_PKG_RE = _re.compile(r"^#\s*package:\s*(\S+)", _re.MULTILINE)

# ---------------------------------------------------------------------------
# R guard stripping — removes interactive/example guards so code always runs
# ---------------------------------------------------------------------------

_GUARD_COND_STARTS = (
    'rlang::is_interactive(',
    'interactive(',
    'FALSE',
    'rlang::is_installed(',
    'requireNamespace(',
)


def _is_guard_opening(stripped_line: str) -> bool:
    """Return True if *stripped_line* opens a known R example guard."""
    if not stripped_line.startswith('if'):
        return False
    after_if = stripped_line[2:].lstrip()
    if not after_if.startswith('('):
        return False
    cond = after_if[1:].lstrip()
    return any(cond.startswith(k) for k in _GUARD_COND_STARTS)


def _extract_inline_body(stripped_line: str) -> str | None:
    """Extract the body from a single-line if-guard (no braces)."""
    after_if = stripped_line[2:].lstrip()
    depth = 0
    for idx, ch in enumerate(after_if):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                body = after_if[idx + 1:].strip()
                return body if body else None
    return None


def strip_r_guards(source: str) -> str:
    """Strip R interactive/example guards and withAutoprint wrappers.

    Removes if-guards (rlang::is_interactive, interactive, FALSE,
    rlang::is_installed, requireNamespace) and withAutoprint / force wrappers
    so the guarded code executes unconditionally in the sandbox.
    """
    lines = source.splitlines(keepends=True)
    out: list[str] = []
    guard_stack: list[int] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()

        if _is_guard_opening(stripped):
            if '{' in stripped:
                depth = stripped.count('{') - stripped.count('}')
                if depth > 0:
                    guard_stack.append(depth)
                    i += 1
                    continue
                # Braces balanced on one line: extract body between braces.
                m = _re.search(r'\{(.+)\}', stripped)
                if m:
                    body = m.group(1).strip()
                    indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
                    nl = '\n' if lines[i].endswith('\n') else ''
                    out.append(indent + body + nl)
                i += 1
                continue
            else:
                body = _extract_inline_body(stripped)
                if body:
                    indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
                    nl = '\n' if lines[i].endswith('\n') else ''
                    out.append(indent + body + nl)
                i += 1
                continue

        if guard_stack:
            delta = lines[i].count('{') - lines[i].count('}')
            guard_stack[-1] += delta
            if guard_stack[-1] <= 0:
                guard_stack.pop()
                i += 1
                continue

        out.append(lines[i])
        i += 1
    return ''.join(out)

from ..types import CaptureSpec, EffectBundle, EffectClass

# Default capture spec used for full script runs.
DEFAULT_CAPTURE: CaptureSpec = frozenset({
    EffectClass.STDOUT,
    EffectClass.FILES,
    EffectClass.GRAPHICS,
    EffectClass.DATA,
    EffectClass.ENV,
    EffectClass.HTML,
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

    source = strip_r_guards(r_path.read_text(encoding="utf-8"))
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
) -> "tuple[EffectBundle, dict[str, EffectBundle], dict[str, dict]]":
    """Run R source with per-entity checkpoint captures.

    Injects a `.r2py_cp(eid)` call after each entity's last source line.
    The checkpoint function serializes new namespace variables (and graphics count
    delta) to ``_r2py_cp_{eid}.json`` files in the workdir during a single R run.

    Returns ``(full_bundle, entity_bundles, entity_types)`` where
    ``entity_bundles`` maps entity_id → per-entity EffectBundle delta and
    ``entity_types`` maps entity_id → {var_name: {"class": ..., "typeof": ...}}.
    Falls back silently: if jsonlite is unavailable or the R run fails,
    ``entity_bundles`` and ``entity_types`` are empty.
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
    r_cp_preamble = build_r_checkpoint_preamble()

    # Inject `.r2py_cp("eid")` after each entity's last line (bottom-up to keep
    # line numbers stable for earlier insertions).
    lines = r_source.splitlines(keepends=True)
    # Bottom-up: process in reverse end_line order.
    for end_line_0, eid in reversed(entity_boundaries):
        insert_after = min(end_line_0, len(lines) - 1)
        safe_eid = eid.replace('"', '\\"').replace("\\", "\\\\")
        checkpoint_line = f'\n.r2py_cp("{safe_eid}")\n'
        lines.insert(insert_after + 1, checkpoint_line)

    checkpointed_source = strip_r_guards("".join(lines))

    # If the script has crawler metadata naming its source package, pre-load
    # that package so its own examples can find their unexported symbols.
    _pkg_match = _CRAWLER_PKG_RE.search(r_source)
    if _pkg_match:
        _pkg_lib = f'suppressPackageStartupMessages(library({_pkg_match.group(1)}))\n'
        checkpointed_source = _pkg_lib + checkpointed_source
        r_source = _pkg_lib + r_source

    with TempWorkdir() as workdir:
        sandbox = RSandbox()
        try:
            full_bundle = sandbox.run(
                checkpointed_source,
                workdir=workdir,
                capture=capture,
                preamble=r_cp_preamble,
                epilogue=_R_CHECKPOINT_EPILOGUE,
                timeout_s=timeout_s,
            )
        except Exception:
            # If the checkpointed run fails, fall back to plain run.
            full_bundle = sandbox.run(
                strip_r_guards(r_source),
                workdir=workdir,
                capture=capture,
                timeout_s=timeout_s,
            )
            return full_bundle, {}, {}

        # Parse per-entity checkpoint files.
        entity_bundles: dict[str, EffectBundle] = {}
        entity_types: dict[str, dict] = {}
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
                # Load per-entity PNG snapshot if present so the comparator can
                # run SSIM. Falls back to the count int when the snapshot is
                # missing or suspiciously small.
                #
                # A PNG ≤ 2 KB at 800×600 is almost certainly a blank
                # dev.copy() artefact (the fallback path in .r2py_cp when
                # close+reopen failed): the primary close-device approach
                # produces real plots well above this threshold.
                _MIN_REAL_PLOT_BYTES = 2000
                plot_path = workdir / f"_r2py_cp_plot_{safe_eid}.png"
                if plot_path.exists():
                    try:
                        _plot_bytes = plot_path.read_bytes()
                        if len(_plot_bytes) >= _MIN_REAL_PLOT_BYTES:
                            graphics_field: object = [_plot_bytes]
                        else:
                            import warnings as _warnings
                            _warnings.warn(
                                f"r2py: per-entity R plot for '{eid}' is only "
                                f"{len(_plot_bytes)} B (≤ {_MIN_REAL_PLOT_BYTES} B). "
                                "This is likely a blank dev.copy() artefact — "
                                "the close-and-reopen capture probably failed for "
                                "this entity. Falling back to count-based matching.",
                                RuntimeWarning,
                                stacklevel=2,
                            )
                            graphics_field = cp_data.get("graphics", 0)
                    except OSError:
                        graphics_field = cp_data.get("graphics", 0)
                else:
                    graphics_field = cp_data.get("graphics", 0)
                raw_stdout = cp_data.get("stdout", "")
                if raw_stdout:
                    raw_stdout = "\n".join(
                        ln for ln in raw_stdout.splitlines()
                        if not ln.lstrip("> ").startswith(".r2py_cp(")
                    )
                eb = EffectBundle(
                    data=raw_data,
                    stdout=raw_stdout,
                    graphics=graphics_field,
                )
                entity_bundles[eid] = eb
                types_data = cp_data.get("types", {})
                if isinstance(types_data, dict) and types_data:
                    entity_types[eid] = types_data
            except Exception:
                continue

        return full_bundle, entity_bundles, entity_types


# Static part of the R checkpoint preamble: state variables, stdout sink, and
# .r2py_cp() function body.  The serializer function (.r2py_serialize_var) is
# prepended at call time by build_r_checkpoint_preamble() so both paths share
# one central implementation from stage0.effects.data.
_R_CHECKPOINT_BODY = r"""
.r2py_prev_vars <- character(0)
.r2py_plot_count <- 0L
.r2py_prev_fig_count <- 0L
.r2py_stdout_buf <- character(0)
.r2py_prev_stdout_len <- 0L

# Count plot/figure creation to mirror Python's len(plt.get_fignums()) semantics.
# `plot.new` fires for base graphics; `grid.newpage` fires for grid-based systems
# (ggplot2, lattice). Counting open devices (dev.list()) does NOT work because the
# graphics preamble pre-opens a single PNG device that subsequent plots share.
local({
  .inc <- function() {
    .r2py_plot_count <<- .r2py_plot_count + 1L
  }
  setHook("plot.new", .inc, action = "append")
  tryCatch(setHook("grid.newpage", .inc, action = "append"),
           error = function(e) NULL)
})

# Redirect stdout into a text connection so we can capture per-entity deltas.
.r2py_stdout_con <- textConnection(".r2py_stdout_buf", open = "w", local = FALSE)
sink(.r2py_stdout_con, type = "output", append = FALSE)

.r2py_cp <- function(eid) {
  tryCatch({
    cur_vars <- setdiff(
      ls(envir = .GlobalEnv),
      c(".r2py_prev_vars", ".r2py_plot_count", ".r2py_prev_fig_count", ".r2py_cp",
        ".r2py_stdout_buf", ".r2py_stdout_con", ".r2py_prev_stdout_len",
        ".r2py_serialize_var")
    )
    new_vars <- setdiff(cur_vars, .r2py_prev_vars)
    data_parts <- character(0)
    uncapturable_vars <- character(0)
    for (v in new_vars) {
      obj <- get(v, envir = .GlobalEnv)
      serialized <- .r2py_serialize_var(obj)
      if (is.null(serialized) || identical(serialized, "__uncapturable__")) {
        uncapturable_vars <- c(uncapturable_vars, v)
      } else {
        # .r2py_serialize_var now returns an R object; encode it here so the
        # per-checkpoint JSON document is well-formed.
        json_val <- jsonlite::toJSON(serialized, auto_unbox = TRUE, na = 'null', force = TRUE)
        data_parts <- c(data_parts, paste0('"', v, '":', as.character(json_val)))
      }
    }
    types_parts <- character(0)
    for (v in new_vars) {
      obj <- get(v, envir = .GlobalEnv)
      cls <- paste(class(obj), collapse = ", ")
      tp <- typeof(obj)
      types_parts <- c(types_parts, paste0('"', v, '":{"class":"', cls, '","typeof":"', tp, '"}'))
    }
    cur_fig_count <- .r2py_plot_count
    # Debounce: collapse to {0,1} per entity. High-level R plotters that use
    # layouts (filled.contour, layout(), par(mfrow=...)) fire plot.new multiple
    # times for one semantic figure; Python's plt.figure() typically fires once.
    # Clamping both sides to 0/1 keeps the count symmetric.
    graphics_delta <- if (cur_fig_count > .r2py_prev_fig_count) 1L else 0L

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

    data_json <- paste0("{", paste(data_parts, collapse = ","), "}")
    types_json <- paste0("{", paste(types_parts, collapse = ","), "}")
    stdout_json <- jsonlite::toJSON(stdout_delta, auto_unbox = TRUE)
    uncapturable_json <- jsonlite::toJSON(uncapturable_vars, auto_unbox = FALSE)
    cp_json <- paste0(
      '{"data":', data_json,
      ',"types":', types_json,
      ',"graphics":', as.integer(graphics_delta),
      ',"stdout":', stdout_json,
      ',"uncapturable":', uncapturable_json,
      "}"
    )
    safe_eid <- gsub("[/:]", "_", eid)
    writeLines(cp_json, paste0("_r2py_cp_", safe_eid, ".json"))

    # If a new plot was drawn during this entity, capture it to a per-entity PNG
    # so the comparator can run SSIM rather than just count-matching.
    #
    # Many R plot functions (filled.contour, image, contour, …) call plot.new()
    # internally and then clear the graphics display list before returning.
    # This makes dev.copy() and recordPlot() unreliable — they replay an empty
    # display list and produce a near-blank PNG (~560 B for an 800×600 device).
    #
    # The only reliable approach is to *close* the current PNG device (which
    # flushes the rendered pixel buffer to disk), copy the resulting file to a
    # per-entity snapshot, then *reopen* the device for subsequent entities.
    if (graphics_delta == 1L) {
      tryCatch({
        grDevices::dev.off()
        plot_file <- file.path(getwd(),
          sprintf("_r2py_plot_%03d.png", .r2py_plot_idx))
        file.copy(plot_file,
          paste0("_r2py_cp_plot_", safe_eid, ".png"),
          overwrite = TRUE)
        grDevices::png(filename = plot_file, width = 800L, height = 600L)
      }, error = function(e) {
        # Fallback: dev.copy (less reliable, but non-destructive).
        tryCatch({
          grDevices::dev.copy(grDevices::png,
            filename = paste0("_r2py_cp_plot_", safe_eid, ".png"),
            width = 800, height = 600)
          grDevices::dev.off()
        }, error = function(e) NULL)
      })
    }

    .r2py_prev_vars <<- cur_vars
    .r2py_prev_fig_count <<- cur_fig_count
    .r2py_prev_stdout_len <<- cur_len
  }, error = function(e) invisible(NULL))
}
"""


# Epilogue appended after the checkpointed user source (runs before R_EPILOGUE).
#
# When .r2py_cp() closes and reopens the PNG device, the reopened device
# starts blank.  If nothing is drawn after the last checkpoint, R_EPILOGUE's
# dev.off() would flush that blank page to disk, losing the global output.
# This epilogue closes the blank device first, then restores the most recent
# real per-entity snapshot as the global plot file so that R_EPILOGUE's
# tryCatch(dev.off(), ...) fails silently — which is harmless.
_R_CHECKPOINT_EPILOGUE = r"""
tryCatch({
  grDevices::dev.off()
  .r2py_plot_file <- file.path(getwd(), sprintf("_r2py_plot_%03d.png", .r2py_plot_idx))
  .r2py_cp_plots <- sort(Sys.glob("_r2py_cp_plot_*.png"))
  if (length(.r2py_cp_plots) > 0L) {
    .r2py_sizes <- vapply(.r2py_cp_plots, file.size, numeric(1L))
    .r2py_real_plots <- .r2py_cp_plots[.r2py_sizes >= 2000L]
    if (length(.r2py_real_plots) > 0L) {
      file.copy(tail(.r2py_real_plots, 1L), .r2py_plot_file, overwrite = TRUE)
    }
  }
}, error = function(e) NULL)
"""


def build_r_checkpoint_preamble() -> str:
    """Return the full R checkpoint preamble for run_script_checkpointed().

    Prepends .r2py_serialize_var() from stage0.effects.data so that per-entity
    checkpoint serialization uses the same adapter dispatch as the global
    epilogue — data frames column-oriented, all other types identical.
    """
    from ..stage0.effects.data import build_r_serializer_fn as _build_serializer
    return _build_serializer() + _R_CHECKPOINT_BODY


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
