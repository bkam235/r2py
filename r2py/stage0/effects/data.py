"""Per-type adapter registry and data capture (§2.2).

The adapter registry is the architectural fix for the v0.1 JSON-opacity trap
(failure.md §2): every non-serializable object type gets a named adapter that
produces a deterministic structured form.  Unknown types go to uncapturable
(EffectBundle.uncapturable), never silently skipped (D2).
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Adapter registry — Python side
# ---------------------------------------------------------------------------

# Each entry: (predicate(obj) -> bool, serializer(obj) -> JSON-serializable value)
_PY_ADAPTERS: list[tuple[Callable[[Any], bool], Callable[[Any], Any]]] = []


def register_py_adapter(
    predicate: Callable[[Any], bool],
    serializer: Callable[[Any], Any],
) -> None:
    """Register a Python-side adapter.  First registered, first checked."""
    _PY_ADAPTERS.append((predicate, serializer))


def _serialize_py(name: str, obj: Any) -> tuple[Any, bool]:
    """Try all adapters.  Returns (serialized_value, ok)."""
    for pred, ser in _PY_ADAPTERS:
        try:
            if pred(obj):
                return ser(obj), True
        except Exception:
            continue
    return None, False


# Built-in Python adapters (registered at module import)
def _is_pandas_df(obj: Any) -> bool:
    try:
        import pandas as pd
        return isinstance(obj, pd.DataFrame)
    except ImportError:
        return False


def _serialize_pandas_df(obj: Any) -> Any:
    import pandas as _pd
    result = {}
    for col in obj.columns:
        series = obj[col]
        if _pd.api.types.is_datetime64_any_dtype(series):
            # Convert datetime64 to ISO date strings matching R's jsonlite format
            result[col] = series.dt.strftime("%Y-%m-%d").tolist()
        else:
            result[col] = series.tolist()
    return result


def _is_pandas_series(obj: Any) -> bool:
    try:
        import pandas as pd
        return isinstance(obj, pd.Series)
    except ImportError:
        return False


def _serialize_pandas_series(obj: Any) -> Any:
    import pandas as _pd
    if _pd.api.types.is_datetime64_any_dtype(obj):
        return obj.dt.strftime("%Y-%m-%d").tolist()
    return obj.tolist()


def _is_numpy_array(obj: Any) -> bool:
    try:
        import numpy as np
        return isinstance(obj, np.ndarray)
    except ImportError:
        return False


def _serialize_numpy_array(obj: Any) -> Any:
    return obj.tolist()


def _is_plain_json(obj: Any) -> bool:
    return isinstance(obj, (bool, int, float, str, list, dict, type(None)))


def _identity(obj: Any) -> Any:
    return obj


def _is_numpy_scalar(obj: Any) -> bool:
    try:
        import numpy as np
        return isinstance(obj, np.generic) and getattr(obj, 'ndim', 1) == 0
    except ImportError:
        return False


def _serialize_numpy_scalar(obj: Any) -> Any:
    return obj.item()


def _is_datetime(obj: Any) -> bool:
    import datetime
    return isinstance(obj, (datetime.date, datetime.datetime))


def _serialize_datetime(obj: Any) -> Any:
    return obj.isoformat()


def _is_pandas_timestamp(obj: Any) -> bool:
    try:
        import pandas as pd
        return isinstance(obj, pd.Timestamp)
    except ImportError:
        return False


def _serialize_pandas_timestamp(obj: Any) -> Any:
    import pandas as _pd
    return None if _pd.isna(obj) else obj.date().isoformat()


def _is_pandas_categorical(obj: Any) -> bool:
    try:
        import pandas as pd
        return isinstance(obj, pd.Categorical)
    except ImportError:
        return False


def _serialize_pandas_categorical(obj: Any) -> Any:
    return list(obj)


# Plain JSON types are checked first so bool/int/str primitives never reach
# downstream adapters. Note bool is a subclass of int — the isinstance check
# in _is_plain_json catches it correctly before any int-specific adapter could.
register_py_adapter(_is_plain_json, _identity)
register_py_adapter(_is_numpy_scalar, _serialize_numpy_scalar)
register_py_adapter(_is_datetime, _serialize_datetime)
register_py_adapter(_is_pandas_timestamp, _serialize_pandas_timestamp)
register_py_adapter(_is_pandas_df, _serialize_pandas_df)
register_py_adapter(_is_pandas_series, _serialize_pandas_series)
register_py_adapter(_is_pandas_categorical, _serialize_pandas_categorical)
register_py_adapter(_is_numpy_array, _serialize_numpy_array)


# ---------------------------------------------------------------------------
# R adapter registry — represented as R code fragments
# ---------------------------------------------------------------------------

# Each entry: (R predicate expression, R serializer expression template)
# Template uses {var} as placeholder for the variable name.
_R_ADAPTERS: list[tuple[str, str]] = []


def register_r_adapter(type_pred: str, serializer: str) -> None:
    """Register an R-side adapter.  type_pred and serializer are R expressions
    using {var} as the placeholder for the variable name."""
    _R_ADAPTERS.append((type_pred, serializer))


# Built-in R adapters
register_r_adapter(
    "is.data.frame({var})",
    "jsonlite::toJSON({var}, dataframe='columns', auto_unbox=TRUE, na='null')",
)
register_r_adapter(
    "inherits({var}, 'htmltools_tag') || inherits({var}, 'shiny.tag')",
    "as.character(htmltools::renderTags({var})$html)",
)
register_r_adapter(
    "inherits({var}, 'lm') || inherits({var}, 'glm')",
    (
        "jsonlite::toJSON(list("
        "  coefficients=as.list(coef({var})),"
        "  residuals=as.list(residuals({var})),"
        "  fitted=as.list(fitted({var}))"
        "), auto_unbox=TRUE)"
    ),
)
register_r_adapter(
    "isS4({var})",
    "jsonlite::toJSON(as.list({var}), auto_unbox=TRUE)",
)
register_r_adapter(
    "is.list({var}) || is.vector({var}) || is.numeric({var}) || is.character({var}) || is.logical({var})",
    "jsonlite::toJSON({var}, auto_unbox=TRUE, na='null')",
)


# ---------------------------------------------------------------------------
# Preamble / epilogue generators
# ---------------------------------------------------------------------------

R_PREAMBLE = """\
library(jsonlite)
.r2py_uncapturable <- character(0)
"""


def build_r_epilogue() -> str:
    """Build the R data capture epilogue from the current _R_ADAPTERS registry.

    Called at sandbox run-time so that adapters registered after module import
    (e.g. by user code or tests) are included.  The generated R code walks
    .GlobalEnv, applies the first matching adapter to each variable, and writes
    _r2py_state.json + _r2py_uncapturable.json.
    """
    # Build if/else dispatch chain from registered adapters
    dispatch_lines: list[str] = []
    for i, (pred_tmpl, ser_tmpl) in enumerate(_R_ADAPTERS):
        pred = pred_tmpl.replace("{var}", ".r2py_obj")
        ser = ser_tmpl.replace("{var}", ".r2py_obj")
        keyword = "if" if i == 0 else "} else if"
        dispatch_lines.append(f"      {keyword} ({pred}) {{")
        dispatch_lines.append(f"        tryCatch({ser}, error = function(e) '__uncapturable__')")
    if dispatch_lines:
        dispatch_lines.append("      } else {")
        dispatch_lines.append("        '__uncapturable__'")
        dispatch_lines.append("      }")
    else:
        dispatch_lines.append("      '__uncapturable__'")
    dispatch = "\n".join(dispatch_lines)

    return (
        "# r2py data capture: serialize all globals to _r2py_state.json\n"
        ".r2py_state <- list()\n"
        ".r2py_vars <- ls(envir = .GlobalEnv)\n"
        ".r2py_vars <- .r2py_vars[!startsWith(.r2py_vars, '.r2py_')]\n"
        "for (.r2py_v in .r2py_vars) {\n"
        "  .r2py_obj <- get(.r2py_v, envir = .GlobalEnv)\n"
        "  .r2py_serialized <- tryCatch({\n"
        "    if (is.function(.r2py_obj) || is.environment(.r2py_obj)) {\n"
        "      NULL\n"
        "    } else {\n"
        + dispatch + "\n"
        "    }\n"
        "  }, error = function(e) '__uncapturable__')\n"
        "  if (identical(.r2py_serialized, '__uncapturable__') || is.null(.r2py_serialized)) {\n"
        "    .r2py_uncapturable <- c(.r2py_uncapturable, .r2py_v)\n"
        "  } else {\n"
        "    .r2py_state[[.r2py_v]] <- .r2py_serialized\n"
        "  }\n"
        "}\n"
        "writeLines(jsonlite::toJSON(.r2py_state, auto_unbox=TRUE), '_r2py_state.json')\n"
        "writeLines(jsonlite::toJSON(.r2py_uncapturable), '_r2py_uncapturable.json')\n"
    )

PY_EPILOGUE_TEMPLATE = """\
import json as _r2py_json

_r2py_state = {}
_r2py_uncapturable = []

for _r2py_k, _r2py_v in list(globals().items()):
    if _r2py_k.startswith('_r2py_') or _r2py_k.startswith('__'):
        continue
    if callable(_r2py_v) and not isinstance(_r2py_v, type):
        continue
    try:
        _r2py_serialized, _r2py_ok = _r2py_try_adapters(_r2py_k, _r2py_v)
        if not _r2py_ok:
            _r2py_uncapturable.append(_r2py_k)
            continue
        _r2py_json.dumps(_r2py_serialized)
        _r2py_state[_r2py_k] = _r2py_serialized
    except Exception:
        _r2py_uncapturable.append(_r2py_k)

try:
    with open('_r2py_state.json', 'w', encoding='utf-8') as _f:
        _r2py_json.dump(_r2py_state, _f)
except Exception:
    _r2py_clean = {}
    for _r2py_k2, _r2py_v2 in _r2py_state.items():
        try:
            _r2py_json.dumps(_r2py_v2)
            _r2py_clean[_r2py_k2] = _r2py_v2
        except Exception:
            _r2py_uncapturable.append(_r2py_k2)
    with open('_r2py_state.json', 'w', encoding='utf-8') as _f:
        _r2py_json.dump(_r2py_clean, _f)
with open('_r2py_uncapturable.json', 'w', encoding='utf-8') as _f:
    _r2py_json.dump(_r2py_uncapturable, _f)
"""


def build_py_preamble() -> str:
    """Build the Python preamble that installs the adapter-lookup helper."""
    adapter_setup = """\
import json as _r2py_json

def _r2py_try_adapters(name, obj):
    \"\"\"Try registered adapters; return (value, True) or (None, False).\"\"\"
    import json
    # plain JSON-serializable scalars
    if isinstance(obj, (bool, int, float, str, type(None))):
        return obj, True
    # numpy scalars and arrays — before generic json.dumps which rejects them
    try:
        import numpy as _np
        if isinstance(obj, _np.generic):
            return obj.item(), True
        if isinstance(obj, _np.ndarray):
            return obj.tolist(), True
    except ImportError:
        pass
    # datetime — datetime before date because datetime is a subclass of date
    try:
        import datetime as _dt
        if isinstance(obj, _dt.datetime):
            return obj.isoformat(), True
        if isinstance(obj, _dt.date):
            return obj.isoformat(), True
    except ImportError:
        pass
    # pandas
    try:
        import pandas as _pd
        if isinstance(obj, _pd.Timestamp):
            return None if _pd.isna(obj) else obj.date().isoformat(), True
        if isinstance(obj, _pd.DataFrame):
            _r2py_result = {}
            for _r2py_col in obj.columns:
                _r2py_series = obj[_r2py_col]
                if _pd.api.types.is_datetime64_any_dtype(_r2py_series):
                    _r2py_result[_r2py_col] = _r2py_series.dt.strftime('%Y-%m-%d').tolist()
                else:
                    _r2py_result[_r2py_col] = _r2py_series.tolist()
            return _r2py_result, True
        if isinstance(obj, _pd.Series):
            if _pd.api.types.is_datetime64_any_dtype(obj):
                return obj.dt.strftime('%Y-%m-%d').tolist(), True
            return obj.tolist(), True
        if isinstance(obj, _pd.Categorical):
            return list(obj), True
    except ImportError:
        pass
    # generic: try json.dumps to test serializability
    try:
        json.dumps(obj)
        return obj, True
    except (TypeError, ValueError):
        pass
    return None, False
"""
    return adapter_setup


# ---------------------------------------------------------------------------
# Collect
# ---------------------------------------------------------------------------

def collect(workdir: Path) -> dict:
    """Read _r2py_state.json and _r2py_uncapturable.json → EffectBundle fields."""
    import json

    data: dict = {}
    uncapturable: list[str] = []

    state_file = workdir / "_r2py_state.json"
    if state_file.exists():
        try:
            raw = json.loads(state_file.read_text(encoding="utf-8"))
            # R epilogue stores values as JSON strings (from jsonlite::toJSON);
            # decode them so data holds Python objects, not strings.
            for k, v in raw.items():
                if isinstance(v, str):
                    try:
                        data[k] = json.loads(v)
                    except (json.JSONDecodeError, ValueError):
                        data[k] = v
                else:
                    data[k] = v
        except Exception:
            pass

    unc_file = workdir / "_r2py_uncapturable.json"
    if unc_file.exists():
        try:
            uncapturable = json.loads(unc_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    return {"data": data, "uncapturable": uncapturable}
