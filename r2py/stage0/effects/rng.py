"""RNG hook preamble/epilogue for capture and replay (§2.2, §2.3)."""
from __future__ import annotations

import json
from pathlib import Path

from ..sandbox.base import ReplayLog


# ---------------------------------------------------------------------------
# R — capture mode
# ---------------------------------------------------------------------------

# Record every draw R makes, in order, so Python can be served the same numbers (the draws are inputs, like
# datasets).  The wrappers pass their arguments through unchanged and are attached ahead of base/stats rather
# than defined in the global environment, so they are not variables of the script.  Calls made inside packages
# or as ``stats::rnorm`` are not recorded.
RNG_FUNCTIONS = (
    "runif", "rnorm", "rexp", "rgamma", "rbeta", "rbinom", "rpois", "rt", "rchisq", "rlnorm", "rweibull",
    "rcauchy", "rgeom", "rlogis", "rnbinom", "sample", "sample.int",
)

R_PREAMBLE_CAPTURE = """\
# r2py RNG capture: log the draws of the common random functions
.r2py_rng_log <- list()
local({
  .names <- c(%s)
  .wrappers <- list()
  for (.n in .names) {
    local({
      .name <- .n
      .orig <- get(.n, envir = globalenv(), mode = 'function')   # base or stats, as found on the search path
      .wrappers[[.name]] <<- function(...) {
        r <- .orig(...)
        if (length(r) <= 100000L) {   # a million-draw vector is not recorded: it would dominate every bundle
          .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(
            fn = if (.name == 'sample.int') 'sample' else .name,
            value = if (is.numeric(r)) as.numeric(r) else as.character(r))
        }
        r
      }
    })
  }
  attach(.wrappers, name = 'r2py:rng', warn.conflicts = FALSE)
})
""" % ", ".join(f"'{n}'" for n in RNG_FUNCTIONS)

R_EPILOGUE_CAPTURE = """\
writeLines(jsonlite::toJSON(.r2py_rng_log, auto_unbox=TRUE, digits=NA), '_r2py_rng.json')
"""


def r_preamble(seed: int | None = None, replay: ReplayLog | None = None) -> str:
    if replay is not None:
        return _r_replay_preamble(replay)
    lines = [R_PREAMBLE_CAPTURE]
    if seed is not None:
        lines.append(f"set.seed({seed}L)\n")
    return "".join(lines)


def _r_replay_preamble(replay: ReplayLog) -> str:
    """Inject pre-recorded RNG draws as a fixed sequence."""
    draws_json = json.dumps([[t[0], t[1], t[2]] for t in replay.rng_draws])
    return f"""\
# r2py RNG replay: use pre-recorded draws
.r2py_rng_replay <- {draws_json}
.r2py_rng_idx <- 1L
set.seed(42L)  # deterministic seed for any non-hooked calls
"""


# ---------------------------------------------------------------------------
# Python — capture mode
# ---------------------------------------------------------------------------

PY_PREAMBLE_CAPTURE = """\
import random as _r2py_random_mod
import functools as _r2py_functools
_r2py_rng_log = []

_r2py_orig_random = _r2py_random_mod.random
def _r2py_hooked_random():
    v = _r2py_orig_random()
    _r2py_rng_log.append(('random', (), v))
    return v
_r2py_random_mod.random = _r2py_hooked_random

try:
    import numpy.random as _r2py_np_random
    _r2py_orig_np_uniform = _r2py_np_random.uniform
    def _r2py_hooked_np_uniform(*args, **kwargs):
        v = _r2py_orig_np_uniform(*args, **kwargs)
        _r2py_rng_log.append(('np.random.uniform', args, v.tolist() if hasattr(v, 'tolist') else v))
        return v
    _r2py_np_random.uniform = _r2py_hooked_np_uniform
except ImportError:
    pass
"""

PY_EPILOGUE_CAPTURE = """\
try:
    import json as _r2py_json_rng
    _r2py_rng_log_ser = [
        [fn, list(args) if args else [], val if not hasattr(val, 'tolist') else val]
        for fn, args, val in _r2py_rng_log
    ]
    with open('_r2py_rng.json', 'w', encoding='utf-8') as _f:
        _r2py_json_rng.dump(_r2py_rng_log_ser, _f)
except Exception:
    pass
"""


def py_preamble(seed: int | None = None, replay: ReplayLog | None = None) -> str:
    if replay is not None:
        return _py_replay_preamble(replay)
    lines = [PY_PREAMBLE_CAPTURE]
    if seed is not None:
        lines.append(f"import random as _r2py_seed_mod; _r2py_seed_mod.seed({seed})\n")
        lines.append(
            f"try:\n    import numpy as _r2py_np_seed; _r2py_np_seed.random.seed({seed})\nexcept ImportError:\n    pass\n"
        )
    return "".join(lines)


def _py_replay_preamble(replay: ReplayLog) -> str:
    """Serve R's recorded draws to Python's random functions (numpy legacy and Generator, stdlib random).

    Draws are queued per R function (``rnorm``, ``runif``, ``sample`` ...).  A Python call that draws ``n``
    values from a distribution takes the first unused R draw of the same family with ``n`` values; with none
    left, or a different count, the real generator answers.  The R values already carry R's parameters
    (mean, sd, bounds), so the Python arguments are not applied.
    """
    queues: dict[str, list] = {}
    for t in replay.rng_draws:
        fn = t[0]
        if isinstance(fn, str) and isinstance(t[2], list):
            queues.setdefault(fn, []).append(t[2])
    return _PY_REPLAY_TEMPLATE.replace("__DRAWS__", json.dumps(queues))


_PY_REPLAY_TEMPLATE = """\
import json as _r2py_json_rp
import sys as _r2py_sys_rp
import math as _r2py_math_rp
import random as _r2py_random_mod
_r2py_rng_log = []
_r2py_draws = _r2py_json_rp.loads(\'\'\'__DRAWS__\'\'\')


_R2PY_HOOK_NAMES = {'hooked', 'meth', '<lambda>', '_r2py_take', '_r2py_default_rng', '_r2py_std_choice', '_r2py_std_sample'}


def _r2py_called_from_script():
    # Only the script's own calls are served: numpy, scipy and sklearn draw numbers while they import and run,
    # and those draws must not use up the ones R made for the script.
    f = _r2py_sys_rp._getframe(1)
    while f is not None and (f.f_code.co_name in _R2PY_HOOK_NAMES or f.f_code.co_name.startswith('_r2py')):
        f = f.f_back
    return f is not None and f.f_globals.get('__name__') == '__main__'


def _r2py_size_shape(size):
    if size is None:
        return ()
    return tuple(int(d) for d in size) if hasattr(size, '__iter__') else (int(size),)


def _r2py_take(family, count):
    if not _r2py_called_from_script():
        return None
    q = _r2py_draws.get(family) or []
    for i, vals in enumerate(q):
        if len(vals) == count:
            _r2py_rng_log.append((family, (), vals))
            return q.pop(i)
    return None


def _r2py_count(shape):
    n = 1
    for d in shape:
        n *= int(d)
    return n


def _r2py_shaped(vals, shape, integer):
    try:
        import numpy as _np
        arr = _np.array(vals, dtype=int if integer else float)
        return arr.reshape(shape) if shape else arr.reshape(()).item()
    except ImportError:
        return vals if shape else vals[0]


# (numpy method name, R family, index of the positional ``size`` argument, integer-valued, takes *dims)
_R2PY_NP_METHODS = [
    ('normal', 'rnorm', 2, False, False), ('standard_normal', 'rnorm', 0, False, False),
    ('randn', 'rnorm', None, False, True), ('uniform', 'runif', 2, False, False),
    ('rand', 'runif', None, False, True), ('random', 'runif', 0, False, False),
    ('random_sample', 'runif', 0, False, False), ('ranf', 'runif', 0, False, False),
    ('exponential', 'rexp', 1, False, False), ('standard_exponential', 'rexp', 0, False, False),
    ('gamma', 'rgamma', 2, False, False), ('beta', 'rbeta', 2, False, False),
    ('binomial', 'rbinom', 2, True, False), ('poisson', 'rpois', 1, True, False),
    ('standard_t', 'rt', 1, False, False), ('chisquare', 'rchisq', 1, False, False),
    ('lognormal', 'rlnorm', 2, False, False), ('weibull', 'rweibull', 1, False, False),
    ('standard_cauchy', 'rcauchy', 0, False, False), ('geometric', 'rgeom', 1, True, False),
    ('logistic', 'rlogis', 2, False, False), ('negative_binomial', 'rnbinom', 2, True, False),
]


def _r2py_make_hook(orig, family, size_pos, integer, dims):
    def hooked(*args, **kwargs):
        if dims:
            shape = tuple(int(a) for a in args)
        else:
            size = kwargs.get('size', args[size_pos] if size_pos is not None and len(args) > size_pos else None)
            shape = _r2py_size_shape(size)
        got = _r2py_take(family, _r2py_count(shape))
        if got is None:
            return orig(*args, **kwargs)
        return _r2py_shaped(got, shape, integer)
    return hooked


def _r2py_choice(orig):
    def hooked(a, size=None, replace=True, p=None, *rest, **kwargs):
        shape = _r2py_size_shape(size)
        got = _r2py_take('sample', _r2py_count(shape))
        if got is None:
            return orig(a, size, replace, p, *rest, **kwargs)
        try:
            import numpy as _np
            arr = _np.array(got)
            return arr.reshape(shape) if shape else arr.reshape(()).item()
        except ImportError:
            return got if shape else got[0]
    return hooked


try:
    import numpy as _r2py_np
    _r2py_nr = _r2py_np.random
    for _m, _fam, _pos, _int, _dims in _R2PY_NP_METHODS:
        if hasattr(_r2py_nr, _m):
            setattr(_r2py_nr, _m, _r2py_make_hook(getattr(_r2py_nr, _m), _fam, _pos, _int, _dims))
    if hasattr(_r2py_nr, 'choice'):
        _r2py_nr.choice = _r2py_choice(_r2py_nr.choice)

    def _r2py_subclass_method(unbound, fam, pos, integer, dims):
        def meth(self, *args, **kwargs):
            return _r2py_make_hook(lambda *a, **k: unbound(self, *a, **k), fam, pos, integer, dims)(*args, **kwargs)
        return meth

    # Subclasses of numpy's own types, not wrappers, so isinstance(x, Generator / RandomState) keeps working
    # inside numpy, scipy and sklearn (scipy passes generators back into default_rng).
    if hasattr(_r2py_nr, 'default_rng'):
        _R2PyOrigGen = _r2py_nr.Generator

        class _R2PyGen(_R2PyOrigGen):
            pass

        for _m, _fam, _pos, _int, _dims in _R2PY_NP_METHODS:
            if hasattr(_R2PyOrigGen, _m):
                setattr(_R2PyGen, _m, _r2py_subclass_method(getattr(_R2PyOrigGen, _m), _fam, _pos, _int, _dims))
        _R2PyGen.choice = (lambda orig: lambda self, *a, **k: _r2py_choice(lambda *x, **y: orig(self, *x, **y))(*a, **k))(_R2PyOrigGen.choice)

        _r2py_orig_default_rng = _r2py_nr.default_rng

        def _r2py_default_rng(seed=None):
            real = _r2py_orig_default_rng(seed)
            return seed if isinstance(seed, _R2PyOrigGen) else _R2PyGen(real.bit_generator)
        _r2py_nr.default_rng = _r2py_default_rng

    # np.random.RandomState instances are not hooked: replacing the class breaks isinstance checks in
    # sklearn and numpy (the module-level functions, which use the global state, are).
except ImportError:
    pass


def _r2py_std_one(orig, family):
    def hooked(*args, **kwargs):
        got = _r2py_take(family, 1)
        return got[0] if got is not None else orig(*args, **kwargs)
    return hooked


for _name, _fam in (('random', 'runif'), ('uniform', 'runif'), ('gauss', 'rnorm'),
                    ('normalvariate', 'rnorm'), ('expovariate', 'rexp')):
    setattr(_r2py_random_mod, _name, _r2py_std_one(getattr(_r2py_random_mod, _name), _fam))

_r2py_orig_std_choice = _r2py_random_mod.choice
def _r2py_std_choice(seq):
    got = _r2py_take('sample', 1)
    return got[0] if got is not None else _r2py_orig_std_choice(seq)
_r2py_random_mod.choice = _r2py_std_choice

_r2py_orig_std_sample = _r2py_random_mod.sample
def _r2py_std_sample(population, k, *args, **kwargs):
    got = _r2py_take('sample', int(k))
    return got if got is not None else _r2py_orig_std_sample(population, k, *args, **kwargs)
_r2py_random_mod.sample = _r2py_std_sample
"""


# ---------------------------------------------------------------------------
# Collect
# ---------------------------------------------------------------------------

def collect(workdir: Path) -> dict:
    """Read _r2py_rng.json → EffectBundle.rng_log list of tuples."""
    rng_file = workdir / "_r2py_rng.json"
    if not rng_file.exists():
        return {"rng_log": []}
    try:
        raw = json.loads(rng_file.read_text(encoding="utf-8"))
        # R writes {fn, value} objects (a length-one value is unboxed); Python writes [fn, args, value].
        out = []
        for entry in raw:
            if isinstance(entry, dict):
                val = entry.get("value")
                out.append((entry.get("fn"), [], val if isinstance(val, list) else [val]))
            else:
                out.append(tuple(entry))
        return {"rng_log": out}
    except Exception:
        return {"rng_log": []}
