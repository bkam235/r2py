from pathlib import Path
p = Path("r2py/runtime/difftest.py")
s = p.read_text(encoding="utf-8")

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)

# R side: record the draws each case makes
rep('''.r2py_add <- function(label, args) {
  res <- tryCatch(suppressWarnings(do.call(.r2py_fun, args)), error = function(e) NULL)
  if (is.null(res)) return(invisible())''', '''.r2py_add <- function(label, args) {
  .before <- length(.r2py_rng_log)
  res <- tryCatch(suppressWarnings(do.call(.r2py_fun, args)), error = function(e) NULL)
  if (is.null(res)) return(invisible())
  .draws <- if (length(.r2py_rng_log) > .before) .r2py_rng_log[(.before + 1L):length(.r2py_rng_log)] else list()''')
rep("list(call = label, args = .r2py_json_args(args), expected = ex)", "list(call = label, args = .r2py_json_args(args), expected = ex, draws = .draws)")
rep('''    program += f"suppressPackageStartupMessages(library({package}))\n"
    program += _R_CASES''', '''    program += f"suppressPackageStartupMessages(library({package}))\n"
    program += _rng_effects.R_PREAMBLE_CAPTURE      # the draws a function makes are recorded per case and replayed to Python
    program += _R_CASES''')
rep("from ..stage0.effects import data as _data_effects\n", "from ..stage0.effects import data as _data_effects\nfrom ..stage0.effects import rng as _rng_effects\n")

# Python side: install the replay hooks, then set the queues per case
rep('''        _res = __FUNC__(*_pos, **_kw)''', '''        _r2py_draws.clear()
        for _d in _c.get('draws') or []:
            _r2py_draws.setdefault(_d['fn'], []).append(_d['value'] if isinstance(_d['value'], list) else [_d['value']])
        _res = __FUNC__(*_pos, **_kw)''')
rep('''        bundle = PySandbox().run(source, workdir=wd, capture=frozenset({EffectClass.DATA}), timeout_s=timeout_s,
                                 sidecar_files={"_cases_in.json": json.dumps([{"args": c["args"]} for c in cases])})''',
    '''        bundle = PySandbox().run(source, workdir=wd, capture=frozenset({EffectClass.DATA, EffectClass.RNG}),
                                 timeout_s=timeout_s, replay=ReplayLog(rng_draws=[("rnorm", [], [0.0])]),   # installs the hooks
                                 sidecar_files={"_cases_in.json": json.dumps([{"args": c["args"], "draws": c.get("draws", [])}
                                                                              for c in cases])})''')
rep("    from ..stage0.sandbox.py_sandbox import PySandbox\n", "    from ..stage0.sandbox.base import ReplayLog\n    from ..stage0.sandbox.py_sandbox import PySandbox\n")
p.write_text(s, encoding="utf-8")

q = Path("r2py/runtime/propose.py")
t = q.read_text(encoding="utf-8")
old = '''"not compared; a factor is a list of str). Use only'''
new = '''"not compared; a factor is a list of str). If the R function draws random numbers (sample, runif, rnorm ...), call the "
    "numpy or random equivalents with the same counts and sizes: the test harness serves R's own draws to them, so what "
    "must match is how the draws are used (order, number, indexing). Use only'''
assert t.count(old) == 1
q.write_text(t.replace(old, new), encoding="utf-8")
