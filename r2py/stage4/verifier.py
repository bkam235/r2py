"""Stage 4 verifier orchestrator (§7.1, §7.4)."""
from __future__ import annotations

import ast as _ast
import json as _json
import re as _re
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from ..stage0.effects import bundle as _bundle_mod
from ..stage0.effects.data import serialize_bundle_data
from ..stage0.sandbox.py_sandbox import PySandbox
from ..stage2.stitch import DATA_SHIM_RE
from ..types import (
    CaptureSpec,
    ComparisonDetail,
    ComparatorResult,
    EffectBundle,
    EffectClass,
    EntityId,
    EntityKind,
    EntityScore,
    FeedbackItem,
    ScoreReport,
)
from .comparators import COMPARATORS
from .comparators.data import DataComparator as _DataComparator
from .decompose import make_score_table

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap as _FullScriptMap


# All capturable effect classes for the Python sandbox run.
_ALL_CAPTURE: CaptureSpec = frozenset({
    EffectClass.STDOUT,
    EffectClass.FILES,
    EffectClass.GRAPHICS,
    EffectClass.DATA,
    EffectClass.HTML,
    EffectClass.ENV,
    EffectClass.WARNINGS,
    EffectClass.RNG,
})


def _get_r_bundle(script_map) -> EffectBundle:
    """Aggregate entity actual_bundles from the ScriptMap into one R ground-truth bundle.

    Deduplicates by object identity: all entities produced by Stage 1's main run
    share the same bundle object, so we merge each unique bundle exactly once.
    """
    seen_ids: set[int] = set()
    bundles: list[EffectBundle] = []
    for e in getattr(script_map, "entities", {}).values():
        ab = getattr(e, "actual_bundle", None)
        if ab is not None and id(ab) not in seen_ids:
            seen_ids.add(id(ab))
            bundles.append(ab)
    if bundles:
        return _bundle_mod.merge(bundles)
    # No entity bundles — return empty (all comparators will score as 1.0 empty-vs-empty)
    return EffectBundle()


def _compare_bundles(
    r_bundle: EffectBundle,
    py_bundle: EffectBundle,
    data_compare: str,
    rtol: float,
    atol: float,
) -> dict[EffectClass, ComparatorResult]:
    results: dict[EffectClass, ComparatorResult] = {}

    # STDOUT
    results[EffectClass.STDOUT] = COMPARATORS[EffectClass.STDOUT].compare(
        r_bundle.stdout, py_bundle.stdout
    )

    # WARNINGS
    results[EffectClass.WARNINGS] = COMPARATORS[EffectClass.WARNINGS].compare(
        r_bundle.warnings, py_bundle.warnings
    )

    # ENV
    results[EffectClass.ENV] = COMPARATORS[EffectClass.ENV].compare(
        r_bundle.env, py_bundle.env
    )

    # FILES
    results[EffectClass.FILES] = COMPARATORS[EffectClass.FILES].compare(
        r_bundle.files, py_bundle.files
    )

    # HTML
    results[EffectClass.HTML] = COMPARATORS[EffectClass.HTML].compare(
        r_bundle.html, py_bundle.html
    )

    # GRAPHICS
    results[EffectClass.GRAPHICS] = COMPARATORS[EffectClass.GRAPHICS].compare(
        r_bundle.graphics, py_bundle.graphics
    )

    # DATA — uses configurable data_compare + tolerance
    data_cmp = _DataComparator(data_compare=data_compare, rtol=rtol, atol=atol)
    results[EffectClass.DATA] = data_cmp.compare(
        r_bundle.data, py_bundle.data, uncapturable=py_bundle.uncapturable
    )

    # NETWORK
    results[EffectClass.NETWORK] = COMPARATORS[EffectClass.NETWORK].compare(
        r_bundle.network_log, py_bundle.network_log
    )

    # RNG
    results[EffectClass.RNG] = COMPARATORS[EffectClass.RNG].compare(
        r_bundle.rng_log, py_bundle.rng_log
    )

    # EXIT CODE (error/exception symmetry)
    results[EffectClass.SYNTAX] = COMPARATORS[EffectClass.SYNTAX].compare(
        r_bundle.exit_code, py_bundle.exit_code
    )

    return results


def _build_feedback(
    comparator_results: dict[EffectClass, ComparatorResult],
    entities: dict,
    r_entity_bundles: dict[str, EffectBundle] | None = None,
    py_entity_bundles: dict[str, EffectBundle] | None = None,
) -> list[FeedbackItem]:
    """Convert comparator results into FeedbackItems for Stage 3.

    Triggers on any partial score (score < 1.0), not just hard "fail", so
    pass_via_fallback results (e.g. score=0.603) generate actionable feedback
    instead of leaving Stage 3 with no signal.

    DATA failures: attributed to the specific entity whose name matches the
    failing variable, so Stage 3 targets the right entity.
    GRAPHICS failures: attributed per entity via the per-entity bundles when
    they carry real PNG bytes; the global GRAPHICS broadcast is suppressed in
    that case to avoid double-feedback.
    Other non-DATA effects are broadcast to all entities (whole-script signal).
    """
    items: list[FeedbackItem] = []

    name_to_eid: dict[str, str] = {
        getattr(e, "name", None): eid
        for eid, e in entities.items()
        if getattr(e, "name", None)
    }

    # Build per-entity GRAPHICS feedback when we have real PNG snapshots.
    # When this fires, suppress the global GRAPHICS broadcast below.
    graphics_attributed = False
    if r_entity_bundles and py_entity_bundles:
        from .decompose import _compare_entity_bundles
        for eid in entities:
            r_eb = r_entity_bundles.get(eid)
            py_eb = py_entity_bundles.get(eid)
            if r_eb is None or py_eb is None:
                continue
            r_g = r_eb.graphics
            py_g = py_eb.graphics
            r_has_bytes = isinstance(r_g, list) and any(
                isinstance(b, (bytes, bytearray)) and b for b in r_g
            )
            py_has_bytes = isinstance(py_g, list) and any(
                isinstance(b, (bytes, bytearray)) and b for b in py_g
            )
            if not (r_has_bytes or py_has_bytes):
                continue
            eb_results = _compare_entity_bundles(r_eb, py_eb)
            g_result = eb_results.get(EffectClass.GRAPHICS)
            if g_result is None or g_result.score >= 1.0:
                graphics_attributed = True
                continue
            msg = g_result.explanation or (
                f"per-entity graphics similarity {g_result.score:.3f} "
                "(R plot vs Python figure differ visually for this entity)"
            )
            items.append(FeedbackItem(
                entity_id=eid,
                effect_class=EffectClass.GRAPHICS,
                message=msg,
                score=g_result.score,
            ))
            graphics_attributed = True

    for ec, result in comparator_results.items():
        if result.score >= 1.0:
            continue

        if ec == EffectClass.DATA and result.per_variable:
            for var_name, var_score in result.per_variable.items():
                if var_score >= 1.0:
                    continue
                expl = (
                    _extract_var_explanation(result.explanation, var_name)
                    or f"{var_name}: score {var_score:.3f}"
                )
                target_eid = name_to_eid.get(var_name)
                if target_eid:
                    items.append(FeedbackItem(
                        entity_id=target_eid,
                        effect_class=ec,
                        message=expl,
                        score=var_score,
                    ))
                else:
                    for eid in entities:
                        items.append(FeedbackItem(
                            entity_id=eid,
                            effect_class=ec,
                            message=expl,
                            score=var_score,
                        ))
        elif ec == EffectClass.GRAPHICS and graphics_attributed:
            # Per-entity GRAPHICS feedback already emitted; skip global broadcast.
            continue
        else:
            if not result.explanation:
                continue
            for entity_id in entities:
                items.append(FeedbackItem(
                    entity_id=entity_id,
                    effect_class=ec,
                    message=result.explanation,
                    score=result.score,
                ))

    return items


def _extract_var_explanation(full_explanation: str, var_name: str) -> str | None:
    """Extract the semicolon-delimited fragment for var_name from a joined explanation."""
    for fragment in full_explanation.split(";"):
        fragment = fragment.strip()
        if fragment.startswith(var_name + ":") or fragment.startswith(var_name + "["):
            return fragment
    return None


_TRUNCATE_LIMIT = 500


def _serialize_value(val: object) -> str:
    """Serialize a bundle value to a compact string for prompt inclusion."""
    s = str(val)
    if len(s) > _TRUNCATE_LIMIT:
        s = s[:_TRUNCATE_LIMIT] + f"... ({len(s) - _TRUNCATE_LIMIT} more chars)"
    return s


def _stdout_diff_summary(r_out: str, py_out: str) -> str:
    """Build a concise diff summary between R and Python stdout."""
    r_lines = r_out.splitlines()
    py_lines = py_out.splitlines()
    if not r_out and py_out:
        return f"R produced no output, Python printed {len(py_lines)} line(s)"
    if r_out and not py_out:
        return f"R printed {len(r_lines)} line(s), Python produced no output"
    if len(r_lines) != len(py_lines):
        return f"R printed {len(r_lines)} line(s), Python printed {len(py_lines)} line(s)"
    diffs = []
    for i, (rl, pl) in enumerate(zip(r_lines, py_lines)):
        if rl != pl:
            diffs.append(f"line {i+1}: R={rl[:60]!r} vs Py={pl[:60]!r}")
            if len(diffs) >= 3:
                diffs.append(f"... and more differences")
                break
    return "; ".join(diffs) if diffs else "stdout differs"


def _build_comparisons(
    comparator_results: dict[EffectClass, ComparatorResult],
    r_bundle: EffectBundle,
    py_bundle: EffectBundle,
    entities: dict,
    r_entity_bundles: dict[str, EffectBundle] | None = None,
    py_entity_bundles: dict[str, EffectBundle] | None = None,
) -> list[ComparisonDetail]:
    """Build concrete R-vs-Python comparison details for every failing effect."""
    details: list[ComparisonDetail] = []
    name_to_eid: dict[str, str] = {
        getattr(e, "name", None): eid
        for eid, e in entities.items()
        if getattr(e, "name", None)
    }

    for ec, result in comparator_results.items():
        if result.score >= 1.0:
            continue

        if ec == EffectClass.DATA and result.per_variable:
            for var_name, var_score in result.per_variable.items():
                if var_score >= 1.0:
                    continue
                r_val = _serialize_value(r_bundle.data.get(var_name, "<missing>"))
                py_val = _serialize_value(py_bundle.data.get(var_name, "<missing>"))
                eid = name_to_eid.get(var_name, "")
                diff = (
                    _extract_var_explanation(result.explanation, var_name)
                    or f"score {var_score:.3f}"
                )
                details.append(ComparisonDetail(
                    effect_class=ec, entity_id=eid,
                    r_value=r_val, py_value=py_val,
                    score=var_score, diff_summary=diff,
                ))

        elif ec == EffectClass.STDOUT:
            if r_entity_bundles and py_entity_bundles:
                for eid in entities:
                    r_eb = r_entity_bundles.get(eid)
                    py_eb = py_entity_bundles.get(eid)
                    r_out = (r_eb.stdout if r_eb else "").strip()
                    py_out = (py_eb.stdout if py_eb else "").strip()
                    if r_out == py_out:
                        continue
                    details.append(ComparisonDetail(
                        effect_class=ec, entity_id=eid,
                        r_value=_serialize_value(r_out) or "(empty)",
                        py_value=_serialize_value(py_out) or "(empty)",
                        score=result.score,
                        diff_summary=_stdout_diff_summary(r_out, py_out),
                    ))
            else:
                r_out = r_bundle.stdout.strip()
                py_out = py_bundle.stdout.strip()
                details.append(ComparisonDetail(
                    effect_class=ec, entity_id="",
                    r_value=_serialize_value(r_out) or "(empty)",
                    py_value=_serialize_value(py_out) or "(empty)",
                    score=result.score,
                    diff_summary=_stdout_diff_summary(r_out, py_out),
                ))

        elif ec == EffectClass.GRAPHICS:
            r_count = len(r_bundle.graphics)
            py_count = len(py_bundle.graphics)
            details.append(ComparisonDetail(
                effect_class=ec, entity_id="",
                r_value=f"{r_count} plot(s)",
                py_value=f"{py_count} plot(s)",
                score=result.score,
                diff_summary=result.explanation or f"R produced {r_count} plots, Python produced {py_count}",
            ))

        elif ec == EffectClass.FILES:
            r_files = set(r_bundle.files.keys())
            py_files = set(py_bundle.files.keys())
            details.append(ComparisonDetail(
                effect_class=ec, entity_id="",
                r_value=", ".join(sorted(r_files)) or "(none)",
                py_value=", ".join(sorted(py_files)) or "(none)",
                score=result.score,
                diff_summary=result.explanation or "file outputs differ",
            ))

        elif ec == EffectClass.WARNINGS:
            details.append(ComparisonDetail(
                effect_class=ec, entity_id="",
                r_value="; ".join(r_bundle.warnings) or "(none)",
                py_value="; ".join(py_bundle.warnings) or "(none)",
                score=result.score,
                diff_summary=result.explanation or "warnings differ",
            ))

        elif ec == EffectClass.ENV:
            details.append(ComparisonDetail(
                effect_class=ec, entity_id="",
                r_value=_serialize_value(r_bundle.env) if r_bundle.env else "(none)",
                py_value=_serialize_value(py_bundle.env) if py_bundle.env else "(none)",
                score=result.score,
                diff_summary=result.explanation or "environment state differs",
            ))

        elif ec == EffectClass.HTML:
            details.append(ComparisonDetail(
                effect_class=ec, entity_id="",
                r_value=f"{len(r_bundle.html)} HTML fragment(s)",
                py_value=f"{len(py_bundle.html)} HTML fragment(s)",
                score=result.score,
                diff_summary=result.explanation or "HTML output differs",
            ))

    return details


def get_r_bundle(script_map) -> EffectBundle:
    """Return the aggregated R ground-truth EffectBundle for *script_map*."""
    return _get_r_bundle(script_map)


# ---------------------------------------------------------------------------
# Data-loading shim activation (Option A — see plan file)
# ---------------------------------------------------------------------------

def _activate_data_shim(source: str) -> tuple[str, bool]:
    """Un-comment any ``# r2py:data_shim:*`` blocks in *source*.

    Returns ``(rewritten_source, has_shim)``.  The shim is saved commented-out
    on disk so the artifact is a clean translation; this pass activates it
    in-memory before the sandbox runs the equivalence test.

    The shim's sidecar filename is the caller's responsibility — it was known
    when the shim was emitted and should be threaded through ``verify()``
    rather than reverse-engineered from the rewritten text.
    """
    has_shim = False

    def _sub(m: "_re.Match[str]") -> str:
        nonlocal has_shim
        has_shim = True
        begin = m.group(1)
        body_commented = m.group(2)
        end = m.group(3)
        # Strip a leading ``# `` from each body line (re-activate).
        activated_lines = [
            line[2:] if line.startswith("# ") else line
            for line in body_commented.splitlines()
        ]
        return begin + "\n".join(activated_lines) + "\n" + end

    rewritten = DATA_SHIM_RE.sub(_sub, source)
    return rewritten, has_shim


def _build_sidecar_payload(script_map) -> str:
    """Serialize R-captured data into the same JSON the shim expects to read.

    Delegates to ``stage0.effects.data.serialize_bundle_data`` so the on-disk
    sidecar (loop._write_data_sidecar) and the in-sandbox copy stay in lockstep.

    Entity-named variables are excluded: they are computed results that Python
    must reproduce, not input data.  However, names that the data shim needs
    (input datasets like ``storms``, ``mtcars``) are kept even if they share
    a name with an entity.
    """
    from ..stage2.stitch import collect_shim_needed_names
    data = getattr(get_r_bundle(script_map), "data", {}) or {}
    entity_names = set(getattr(script_map, "entities", {}) or {})
    shim_names = set(collect_shim_needed_names(script_map))
    filtered = {k: v for k, v in data.items()
                if k not in entity_names or k in shim_names}
    return serialize_bundle_data(filtered)


# ---------------------------------------------------------------------------
# Per-entity Python checkpoint injection (Option 2 scoring)
# ---------------------------------------------------------------------------

# Preamble injected before the candidate Python script so _r2py_checkpoint is available.
_PY_CHECKPOINT_PREAMBLE = """\
import json as _r2py_json
import io as _r2py_io
import sys as _r2py_sys

_r2py_prev_ns: set = set()
_r2py_stdout_buf = _r2py_io.StringIO()
_r2py_real_stdout = _r2py_sys.stdout
_r2py_sys.stdout = type('_Tee', (), {
    'write': lambda s, x: (_r2py_stdout_buf.write(x), _r2py_real_stdout.write(x)),
    'flush': lambda s: (_r2py_stdout_buf.flush(), _r2py_real_stdout.flush()),
    'fileno': lambda s: _r2py_real_stdout.fileno(),
})()
_r2py_prev_stdout_pos = 0
_r2py_prev_fig_count = 0

def _r2py_checkpoint(eid):
    global _r2py_prev_ns, _r2py_prev_stdout_pos, _r2py_prev_fig_count
    try:
        import matplotlib.pyplot as _plt
        cur_fig_count = len(_plt.get_fignums())
    except Exception:
        _plt = None
        cur_fig_count = 0
    # Debounce to {0,1}: matches the R side, which clamps to handle layout-using
    # plotters that fire plot.new multiple times per semantic figure.
    graphics_delta = 1 if cur_fig_count > _r2py_prev_fig_count else 0

    safe_eid = eid.replace('/', '_').replace(':', '_')

    # Snapshot the newest figure so the per-entity comparator can run SSIM
    # rather than just count-match.
    if graphics_delta == 1 and _plt is not None:
        try:
            _new_fn = max(_plt.get_fignums())
            _new_fig = _plt.figure(_new_fn)
            _new_fig.set_size_inches(8, 6)
            _new_fig.savefig(f'_r2py_cp_plot_{safe_eid}.png', dpi=100)
        except Exception:
            pass

    # Close all figures after snapshotting so the next entity starts with a
    # clean matplotlib state. Without this, plt.imshow() / plt.plot() in a
    # later entity draws into the previous entity's still-open figure, producing
    # composite images and misleading SSIM scores.
    if _plt is not None:
        try:
            _plt.close('all')
            cur_fig_count = 0
        except Exception:
            pass

    cur_stdout = _r2py_stdout_buf.getvalue()
    stdout_delta = cur_stdout[_r2py_prev_stdout_pos:]

    g = globals()
    new_vars = {}
    uncapturable_vars = []
    for k, v in g.items():
        if k.startswith('_r2py') or k in _r2py_prev_ns:
            continue
        try:
            if callable(v) and not isinstance(v, type):
                _r2py_vtype = type(v)
                _r2py_tname = _r2py_vtype.__name__
                if _r2py_tname in ('function', 'builtin_function_or_method', 'method',
                                    'method-wrapper', 'method_descriptor'):
                    continue
                import inspect as _r2py_inspect
                try:
                    _r2py_sig = _r2py_inspect.signature(v)
                    _r2py_fmls = list(_r2py_sig.parameters.keys())
                except (ValueError, TypeError):
                    _r2py_fmls = []
                if set(_r2py_fmls) <= {'args', 'kwargs', 'self', 'cls'}:
                    for _r2py_wattr in dir(v):
                        if _r2py_wattr.startswith('__') and _r2py_wattr != '__wrapped__':
                            continue
                        _r2py_inner = getattr(v, _r2py_wattr, None)
                        if _r2py_inner is None or not callable(_r2py_inner) or type(_r2py_inner).__name__ != 'function':
                            continue
                        try:
                            _r2py_inner_fmls = list(_r2py_inspect.signature(_r2py_inner).parameters.keys())
                            if not set(_r2py_inner_fmls) <= {'args', 'kwargs', 'self', 'cls'}:
                                _r2py_fmls = _r2py_inner_fmls
                                break
                        except (ValueError, TypeError):
                            pass
                _r2py_meta = {
                    '__r2py_callable_meta__': True,
                    'class': [_r2py_vtype.__name__],
                    'formals': _r2py_fmls,
                    'attributes': {},
                }
                for _r2py_an in ('name', 'dispatch_args'):
                    _r2py_av = getattr(v, _r2py_an, None)
                    if _r2py_av is not None:
                        _r2py_meta['attributes'][_r2py_an] = _r2py_av
                new_vars[k] = _r2py_meta
                continue
            _r2py_serialized, _r2py_ok = _r2py_try_serialize(k, v)
            if not _r2py_ok:
                uncapturable_vars.append(k)
                continue
            if isinstance(_r2py_serialized, dict) and '__r2py_callable_meta__' in _r2py_serialized:
                _r2py_serialized = {_k: _v for _k, _v in _r2py_serialized.items() if _k != '__r2py_callable_meta__'}
            new_vars[k] = _r2py_serialized
        except Exception:
            uncapturable_vars.append(k)

    try:
        with open(f'_r2py_cp_{safe_eid}.json', 'w', encoding='utf-8') as _f:
            _r2py_json.dump({'data': new_vars, 'stdout': stdout_delta,
                             'graphics': graphics_delta,
                             'uncapturable': uncapturable_vars}, _f)
    except Exception:
        pass

    _r2py_prev_ns = set(k for k in g if not k.startswith('_r2py'))
    _r2py_prev_stdout_pos = len(cur_stdout)
    _r2py_prev_fig_count = cur_fig_count
"""


def _inject_py_checkpoints(
    py_source: str,
    entity_line_map: dict[str, tuple[int, int]],
) -> tuple[str, list[str]]:
    """Insert ``_r2py_checkpoint(eid)`` after each entity's last line.

    Inserts bottom-up so earlier line numbers are not disturbed.
    Returns ``(modified_source, ordered_eids)`` where ``ordered_eids`` lists
    the entity ids in ascending end-line order (for checkpoint file collection).
    """
    if not entity_line_map:
        return py_source, []

    lines = py_source.splitlines(keepends=True)
    # Ensure last line has a trailing newline so checkpoint insertion works.
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    # Sort by end_line ascending; process in reverse for bottom-up insertion.
    sorted_pairs = sorted(entity_line_map.items(), key=lambda kv: kv[1][1])
    ordered_eids = [eid for eid, _ in sorted_pairs]

    for eid, (_start, end_line) in reversed(sorted_pairs):
        # entity_line_map uses 1-based line numbers; convert to 0-based index.
        insert_idx = min(end_line, len(lines))  # insert after end_line (1-based → index)
        safe_eid = eid.replace("'", "\\'")
        checkpoint_line = f"_r2py_checkpoint('{safe_eid}')\n"
        candidate = lines[:insert_idx] + [checkpoint_line] + lines[insert_idx:]
        try:
            _ast.parse("".join(candidate))
            lines = candidate
        except SyntaxError:
            # Insertion point is inside an open expression (entity range was clipped
            # mid-expression by overlap resolution). Skip checkpoint to avoid
            # corrupting the source; entity scoring falls back to global score.
            pass

    # Baseline the namespace right before the first entity so that imports
    # and the data shim (which run earlier in the file) are excluded from
    # the first entity's checkpoint delta.
    first_start = sorted_pairs[0][1][0] if sorted_pairs else None
    if first_start is not None:
        baseline_idx = min(first_start - 1, len(lines))  # 1-based → 0-based insert
        lines.insert(baseline_idx, "_r2py_prev_ns = set(k for k in globals() if not k.startswith('_r2py'))\n")

    return "".join(lines), ordered_eids


def _collect_py_checkpoints(
    workdir: "Path",
    eids: list[str],
) -> dict[str, EffectBundle]:
    """Read ``_r2py_cp_{eid}.json`` files from *workdir* and build EffectBundle deltas."""
    import json as _json

    result: dict[str, EffectBundle] = {}
    for eid in eids:
        safe_eid = eid.replace("/", "_").replace(":", "_")
        cp_path = workdir / f"_r2py_cp_{safe_eid}.json"
        if not cp_path.exists():
            continue
        try:
            cp = _json.loads(cp_path.read_text(encoding="utf-8"))
            raw_data = cp.get("data", {})
            # JSON null/array can appear when no new variables were captured; normalise.
            if not isinstance(raw_data, dict):
                raw_data = {}
            plot_path = workdir / f"_r2py_cp_plot_{safe_eid}.png"
            if plot_path.exists():
                try:
                    graphics_field: object = [plot_path.read_bytes()]
                except OSError:
                    graphics_field = cp.get("graphics", 0)
            else:
                graphics_field = cp.get("graphics", 0)
            eb = EffectBundle(
                data=raw_data,
                stdout=cp.get("stdout", "") or "",
                graphics=graphics_field,  # type: ignore[arg-type]
            )
            eb.uncapturable.extend(cp.get("uncapturable", []))
            result[eid] = eb
        except Exception:
            continue
    return result


def verify(
    script_map,
    candidate: str,
    changed: list[str] | None = None,
    data_compare: str = "auto",
    rtol: float = 1e-6,
    atol: float = 1e-9,
    use_fuzz: bool = False,
    fuzz_n: int = 10,
    use_judge: bool = False,
    workdir: Path | None = None,
    timeout_s: float = 60,
    entity_line_map: dict | None = None,
    return_bundle: bool = False,
    sidecar_filename: str | None = None,
    verbose: bool = False,
) -> "ScoreReport | tuple[ScoreReport, EffectBundle]":
    """Score a candidate Python translation against the R ScriptMap.

    changed: entity_ids touched by the last edit; if provided, only those
    entities are re-verified (incremental verification, §7.4).

    sidecar_filename: when the candidate source contains a data-loading shim
    (Option A), this is the basename the shim's ``Path(__file__).parent /
    "<name>"`` lookup expects.  Threaded from the loop (which knows it from
    ``checkpoint_path.stem``); see plans/i-go-with-option-melodic-dewdrop.md.
    """
    entities = getattr(script_map, "entities", {})

    # --- Run candidate in Python sandbox ---
    r_bundle = _get_r_bundle(script_map)

    # Determine which effects were actually captured in R so we capture the same in Python
    capture = _ALL_CAPTURE

    # Inject per-entity checkpoint calls into the Python source (Option 2 scoring).
    py_source_checkpointed, cp_eids = _inject_py_checkpoints(candidate, entity_line_map or {})

    # Rebuild entity_line_map from the checkpointed source so crash attribution
    # line numbers (which reference the checkpointed script) map correctly.
    if entity_line_map:
        from ..stage2.stitch import rebuild_entity_line_map as _rebuild_elmap
        from ..stage2.sentinel_mapper import flatten_entity_line_map as _flatten
        cp_entity_line_map = _flatten(_rebuild_elmap(py_source_checkpointed))
    else:
        cp_entity_line_map = None

    # Activate the data-loading shim (Option A) in the source we hand to the
    # sandbox.  The on-disk artifact stays commented-out; this rewrite affects
    # only the in-memory copy used for equivalence testing.
    py_source_activated, has_shim = _activate_data_shim(py_source_checkpointed)
    sidecar_files: dict[str, str] | None = None
    if has_shim and sidecar_filename:
        payload = _build_sidecar_payload(script_map)
        sidecar_files = {sidecar_filename: payload}

    sandbox = PySandbox()
    if workdir is not None:
        py_bundle = sandbox.run(
            py_source_activated, workdir=workdir, capture=capture,
            preamble=_PY_CHECKPOINT_PREAMBLE, timeout_s=timeout_s,
            sidecar_files=sidecar_files,
        )
        py_entity_bundles = _collect_py_checkpoints(workdir, cp_eids)
    else:
        with tempfile.TemporaryDirectory() as _tmpdir:
            _wd = Path(_tmpdir)
            py_bundle = sandbox.run(
                py_source_activated, workdir=_wd, capture=capture,
                preamble=_PY_CHECKPOINT_PREAMBLE, timeout_s=timeout_s,
                sidecar_files=sidecar_files,
            )
            py_entity_bundles = _collect_py_checkpoints(_wd, cp_eids)

    # R per-entity bundles from Stage 1's checkpointed run.
    r_entity_bundles: dict[str, EffectBundle] = getattr(script_map, "entity_bundles", {})

    # --- Compare bundles ---
    comparator_results = _compare_bundles(r_bundle, py_bundle, data_compare, rtol, atol)

    # --- Score decomposition ---
    score_table = make_score_table(
        entities, comparator_results,
        py_exit_code=py_bundle.exit_code,
        entity_line_map=cp_entity_line_map or entity_line_map,
        py_stderr=py_bundle.stderr,
        preamble_lines=py_bundle.preamble_lines,
        r_entity_bundles=r_entity_bundles or None,
        py_entity_bundles=py_entity_bundles or None,
        data_compare=data_compare,
        rtol=rtol,
        atol=atol,
        verbose=verbose,
    )

    # --- Differential fuzzing (optional) ---
    feedback: list[FeedbackItem] = []
    if use_fuzz:
        from . import fuzz as _fuzz
        fuzz_cfg = _fuzz.FuzzConfig(n_inputs=fuzz_n)
        feedback.extend(_fuzz.run_fuzz(script_map, candidate, config=fuzz_cfg, data_compare=data_compare))

    feedback.extend(_build_feedback(
        comparator_results, entities,
        r_entity_bundles=r_entity_bundles or None,
        py_entity_bundles=py_entity_bundles or None,
    ))

    # Per-entity STDOUT feedback: detect R auto-print vs Python missing print.
    # When R produced stdout for an entity (auto-printed an unassigned expression)
    # but Python produced nothing, generate a targeted hint for that entity so
    # Stage 3 knows exactly what to fix rather than receiving only global noise.
    for eid, r_eb in (r_entity_bundles or {}).items():
        if not r_eb.stdout:
            continue
        py_eb = (py_entity_bundles or {}).get(eid)
        if py_eb is not None and not py_eb.stdout:
            feedback.append(FeedbackItem(
                entity_id=eid,
                effect_class=EffectClass.STDOUT,
                message=(
                    "R auto-prints this expression's result to stdout, "
                    "but Python produces no output for this entity. "
                    "Change the Python code or append to it so that it also prints to stdout."
                ),
                score=0.0,
            ))

    # RC2: surface crash traceback as feedback so Stage 3 knows what line failed.
    # Target the feedback to the entity that caused the crash (via crash attribution)
    # so _weak_first prioritises it. Fall back to all entities if unattributable.
    if py_bundle.exit_code != 0 and py_bundle.stderr:
        crash_msg = py_bundle.stderr.strip()
        if len(crash_msg) > 800:
            crash_msg = "..." + crash_msg[-800:]
        crash_target_ids: list[str] = []
        _crash_elmap = cp_entity_line_map or entity_line_map
        if _crash_elmap:
            from .decompose import _parse_crash_line, _attribute_crash
            crash_line = _parse_crash_line(py_bundle.stderr)
            if crash_line is not None:
                crashing_eid, _ = _attribute_crash(
                    crash_line, py_bundle.preamble_lines, _crash_elmap
                )
                if crashing_eid:
                    crash_target_ids = [crashing_eid]
        if not crash_target_ids:
            crash_target_ids = list(entities.keys())
        for entity_id in crash_target_ids:
            feedback.append(FeedbackItem(
                entity_id=entity_id,
                effect_class=EffectClass.SYNTAX,
                message=f"Python crashed (exit {py_bundle.exit_code}): {crash_msg}",
                score=0.0,
            ))

    # --- Uncomparable entities ---
    uncomparable: list[EntityId] = []
    data_result = comparator_results.get(EffectClass.DATA)
    if data_result and data_result.verdict == "uncomparable":
        uncomparable.extend(entities.keys())

    # Only include effect classes where R actually produced something.
    _r_has_effect = {
        EffectClass.STDOUT:   bool(r_bundle.stdout),
        EffectClass.DATA:     bool(r_bundle.data),
        EffectClass.FILES:    bool(r_bundle.files),
        EffectClass.GRAPHICS: bool(r_bundle.graphics),
        EffectClass.HTML:     bool(r_bundle.html),
        EffectClass.ENV:      bool(r_bundle.env),
        EffectClass.WARNINGS: bool(r_bundle.warnings),
        EffectClass.RNG:      bool(r_bundle.rng_log),
        EffectClass.NETWORK:  bool(r_bundle.network_log),
        EffectClass.SYNTAX:   True,
    }
    by_effect = {
        ec: result.score
        for ec, result in comparator_results.items()
        if _r_has_effect.get(ec, False)
    }

    # --- Aggregate score ---
    # If R succeeded but Python crashed, the scripts are not execution-equivalent.
    # Force aggregate to 0.0 so the agent gets clear feedback to fix the crash.
    if r_bundle.exit_code == 0 and py_bundle.exit_code != 0:
        aggregate = 0.0

        comparisons = _build_comparisons(
            comparator_results, r_bundle, py_bundle, entities,
            r_entity_bundles=r_entity_bundles or None,
            py_entity_bundles=py_entity_bundles or None,
        )

        report = ScoreReport(
            aggregate=aggregate,
            by_entity=score_table,
            by_effect=by_effect,
            uncomparable=uncomparable,
            feedback=feedback,
            comparisons=comparisons,
            py_exit_code=py_bundle.exit_code,
            py_entity_bundles=py_entity_bundles or {},
        )
        if return_bundle:
            return report, py_bundle
        return report

    # Only average entities where R actually produced observable output.
    # Within each entity, only average dimensions backed by effects that
    # THIS ENTITY's R bundle actually produced (per-entity, not global).

    def _entity_r_effects(eid: str) -> dict[EffectClass, bool]:
        """What did R produce for this specific entity?"""
        r_eb = (r_entity_bundles or {}).get(eid)
        if r_eb is None:
            return _r_has_effect  # fallback to global
        r_gfx = r_eb.graphics if isinstance(r_eb.graphics, int) else len(r_eb.graphics or [])
        return {
            EffectClass.DATA:     bool(r_eb.data),
            EffectClass.STDOUT:   bool(r_eb.stdout),
            EffectClass.GRAPHICS: r_gfx > 0,
            EffectClass.FILES:    bool(getattr(r_eb, "files", None)),
            EffectClass.HTML:     bool(getattr(r_eb, "html", None)),
            EffectClass.ENV:      bool(getattr(r_eb, "env", None)),
            EffectClass.WARNINGS: bool(getattr(r_eb, "warnings", None)),
        }

    def _r_entity_has_output(eid: str) -> bool:
        r_eb = (r_entity_bundles or {}).get(eid)
        if r_eb is None:
            return True
        r_gfx = r_eb.graphics if isinstance(r_eb.graphics, int) else len(r_eb.graphics or [])
        return bool(r_eb.data or r_eb.stdout or r_gfx > 0)

    def _active_dims(es: EntityScore) -> frozenset[str]:
        kind = getattr(entities.get(es.entity_id), "kind", None)
        eff = _entity_r_effects(es.entity_id)
        has_data = eff.get(EffectClass.DATA, False)
        has_stdout = eff.get(EffectClass.STDOUT, False)
        has_side = any(eff.get(ec, False) for ec in (
            EffectClass.FILES, EffectClass.GRAPHICS, EffectClass.HTML,
            EffectClass.ENV, EffectClass.WARNINGS,
        ))
        names: list[str] = []
        if kind in (EntityKind.VARIABLE, EntityKind.CONSTANT,
                    EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
            if has_data:
                names.append("type_match")
        else:
            names.append("type_match")
        if kind == EntityKind.FUNCTION_DEF:
            if has_stdout:
                names.append("control_flow_match")
        elif kind in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
            if has_data:
                names.append("control_flow_match")
        else:
            names.append("control_flow_match")
        if has_data:
            names.extend(("data_output", "variable_output"))
        if kind in (EntityKind.FUNCTION_DEF, EntityKind.FUNCTION_CALL,
                    EntityKind.EXTERNAL_SYMBOL):
            if has_data:
                names.append("callable_output")
        if has_side:
            names.append("side_effects")
        if has_stdout and not has_data and not has_side:
            names.append("side_effects")
        return frozenset(names)

    def _weighted_entity_avg(es: EntityScore) -> float:
        ad = es.active_dims
        vals = [getattr(es, name) for name in ad]
        if not vals:
            return float(es.executed_ok)
        return sum(vals) / len(vals)

    entity_scores = list(score_table.values())
    for es in entity_scores:
        es.active_dims = _active_dims(es)
    if entity_scores:
        contributing = [
            _weighted_entity_avg(es)
            for es in entity_scores
            if _r_entity_has_output(es.entity_id)
        ]
        if not contributing:
            contributing = [_weighted_entity_avg(es) for es in entity_scores]
        aggregate = sum(contributing) / len(contributing)
    else:
        scored_results = [
            r for ec, r in comparator_results.items()
            if r.verdict != "uncomparable" and _r_has_effect.get(ec, False)
        ]
        aggregate = sum(r.score for r in scored_results) / len(scored_results) if scored_results else 1.0

    comparisons = _build_comparisons(
        comparator_results, r_bundle, py_bundle, entities,
        r_entity_bundles=r_entity_bundles or None,
        py_entity_bundles=py_entity_bundles or None,
    )

    report = ScoreReport(
        aggregate=aggregate,
        by_entity=score_table,
        by_effect=by_effect,
        uncomparable=uncomparable,
        feedback=feedback,
        comparisons=comparisons,
        py_exit_code=py_bundle.exit_code,
        py_entity_bundles=py_entity_bundles or {},
    )
    if return_bundle:
        return report, py_bundle
    return report
