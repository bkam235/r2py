"""RNG hook preamble/epilogue for capture and replay (§2.2, §2.3)."""
from __future__ import annotations

import json
from pathlib import Path

from ..sandbox.base import ReplayLog


# ---------------------------------------------------------------------------
# R — capture mode
# ---------------------------------------------------------------------------

# Replace the most common base RNG functions with logging stubs that call
# through to the originals.  This covers the majority of scripts; calls via
# base::runif() or inside packages will not be logged (acceptable for replay).
R_PREAMBLE_CAPTURE = """\
# r2py RNG capture: replace common RNG functions with logging stubs
.r2py_rng_log <- list()
.r2py_orig_runif  <- base::runif
.r2py_orig_rnorm  <- base::rnorm
.r2py_orig_sample <- base::sample
.r2py_orig_rbinom <- base::rbinom
.r2py_orig_rpois  <- base::rpois
.r2py_orig_rexp   <- base::rexp
.r2py_orig_runif.default  <- base::runif

runif <- function(n, min = 0, max = 1) {
  r <- .r2py_orig_runif(n, min, max)
  .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(fn="runif", args=list(n=n,min=min,max=max), value=as.list(r))
  r
}
rnorm <- function(n, mean = 0, sd = 1) {
  r <- .r2py_orig_rnorm(n, mean, sd)
  .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(fn="rnorm", args=list(n=n,mean=mean,sd=sd), value=as.list(r))
  r
}
sample <- function(x, size, replace = FALSE, prob = NULL) {
  r <- if (missing(size)) .r2py_orig_sample(x) else .r2py_orig_sample(x, size, replace, prob)
  .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(fn="sample", args=list(x=x), value=as.list(r))
  r
}
rbinom <- function(n, size, prob) {
  r <- .r2py_orig_rbinom(n, size, prob)
  .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(fn="rbinom", args=list(n=n,size=size,prob=prob), value=as.list(r))
  r
}
rpois <- function(n, lambda) {
  r <- .r2py_orig_rpois(n, lambda)
  .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(fn="rpois", args=list(n=n,lambda=lambda), value=as.list(r))
  r
}
rexp <- function(n, rate = 1) {
  r <- .r2py_orig_rexp(n, rate)
  .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(fn="rexp", args=list(n=n,rate=rate), value=as.list(r))
  r
}
"""

R_EPILOGUE_CAPTURE = """\
writeLines(jsonlite::toJSON(.r2py_rng_log, auto_unbox=TRUE), '_r2py_rng.json')
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
    draws_json = json.dumps([[t[0], t[1], t[2]] for t in replay.rng_draws])
    return f"""\
import random as _r2py_random_replay
_r2py_replay_draws = {draws_json}
_r2py_replay_idx = 0

_r2py_orig_random_replay = _r2py_random_replay.random
def _r2py_replayed_random():
    global _r2py_replay_idx
    if _r2py_replay_idx < len(_r2py_replay_draws):
        val = _r2py_replay_draws[_r2py_replay_idx][2]
        _r2py_replay_idx += 1
        return val
    return _r2py_orig_random_replay()
_r2py_random_replay.random = _r2py_replayed_random
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
        return {"rng_log": [tuple(entry) for entry in raw]}
    except Exception:
        return {"rng_log": []}
