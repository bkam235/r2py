# Approach for diagnosis 5 — make model objects comparable instead of excluded

## The problem, precisely

`r2py/stage4/comparators/data.py:255` drops any variable the Python side could not
serialize:

```
[r2py] WARNING: 'glmModel' is a data entity but Python could not serialize it — excluded from comparison
```

1,278 occurrences in the training run, 75 distinct names, **30% of scripts affected**.
The top names are fitted models and pipelines: `glmModel`, `model`, `kpca_estimates`,
`rec` (recipe), `rocobj` (pROC), `irisFit*`, `fit*`.

The asymmetry is the root cause:

- **R side** (`stage0/effects/data.py`): an `lm`/`glm` object satisfies `is.list()`, so the
  generic list adapter serialises it — recursively dumping `coefficients`, `residuals`,
  `fitted.values`, but also `qr`, `terms`, `model`, `call`. R captures a large nested blob.
- **Python side** (`_R2PyEncoder` / `_r2py_try_serialize`): a statsmodels results object or
  sklearn estimator is not JSON-serialisable and no `default()` branch handles it, so it is
  routed to `uncapturable` and the comparator skips it.

So the entity is silently removed from the score. It neither helps nor hurts — it simply
isn't measured. That is why the `stats_objects` stratum looks deceptively fine.

Note that R's raw nested dump is **not** the right comparison target either: `qr`
decompositions, `terms` objects and captured environments have no Python counterpart. Dumping
more of the Python object would not make the two sides comparable.

## The approach: a canonical fingerprint on both sides

Instead of serialising *the object*, both sides emit the same small, semantically
meaningful projection — a **model fingerprint** — and the comparator compares those.

```python
{
  "__r2py_model__": "linear_model",          # canonical family, not the library's class
  "coefficients": {"(Intercept)": 3.21, "wt": -0.87},
  "fitted":       [...],                     # numeric vector, length n
  "residuals":    [...],
  "n_obs":        32,
  "df_residual":  30,
  "sigma":        0.48,
  "family":       "gaussian",
  "link":         "identity",
  "formula":      "mpg ~ wt",
}
```

Rules that make this work:

- **Canonical family names**, not class names. R `lm` and statsmodels `OLS` both map to
  `linear_model`; R `glm` and statsmodels `GLM`/sklearn `LogisticRegression` map to
  `glm`. The comparator first checks the families agree.
- **Normalised coefficient keys.** `(Intercept)` ↔ `const` ↔ `Intercept` collapse to one
  canonical key. Without this every regression scores 0 on a naming artefact.
- **Label-invariant fields where labels are arbitrary.** For clustering, compare *sorted*
  cluster sizes and centres ordered canonically — k-means label 1 in R is not label 1 in
  sklearn, and comparing raw labels would be meaningless.
- **Field-wise scoring over the intersection.** The score is the mean over fields present on
  *both* sides, and the comparator reports which fields were compared. A fingerprint that
  only yields `n_obs` on one side scores on `n_obs` alone — and says so, so thin coverage is
  visible rather than hidden.
- **Numeric tolerance** reuses the comparator's existing `rtol`/`atol`.

### Per-family fingerprints

| Family | Fields | Notes |
|---|---|---|
| `linear_model` | coefficients, fitted, residuals, n_obs, df_residual, sigma | R `lm` ↔ statsmodels OLS |
| `glm` | + family, link, deviance, aic | R `glm` ↔ statsmodels GLM / sklearn |
| `roc` | auc, sensitivities, specificities, thresholds | pROC ↔ sklearn `roc_curve` |
| `preprocessor` | steps (ordered names), n_vars, outcome | recipes ↔ sklearn Pipeline |
| `clustering` | k, sorted cluster_sizes, centres (canonical order) | kmeans/bclust ↔ sklearn |
| `survival_curve` | time, surv, n_risk, n_event | prodlim/Hist ↔ lifelines |
| `decomposition` | sdev/explained_variance, n_components | kpca/prcomp ↔ sklearn |

## Where the code goes

**R side** — `r2py/stage0/effects/data.py` already has the right extension point:

```python
register_r_adapter("is.list({var})", "lapply({var}, .r2py_serialize_var)")
```

Adapters dispatch **in registration order**, and `lm` satisfies `is.list()`. So model
adapters must be consulted *before* the generic list adapter. Two options:

- add a `priority` argument to `register_r_adapter` and sort by it, or
- keep a separate `_R_MODEL_ADAPTERS` list that `build_r_serializer_fn()` emits first.

The second is less invasive and keeps the existing registry semantics untouched.

**Python side** — `_R2PyEncoder.default()` inside `PY_EPILOGUE_TEMPLATE`. `default()` is
called precisely for objects JSON cannot handle, which is exactly our case. Add a
`_r2py_model_fingerprint(obj)` helper tried first in `default()`, with guarded imports in the
style of the existing numpy/pandas blocks (statsmodels and sklearn must stay optional).

Because this code is injected as *source text* into the generated script, the adapters must be
written as strings in the template and cannot rely on anything installed in the r2py venv
alone — they must degrade to today's behaviour when the library is absent.

**Comparator** — `r2py/stage4/comparators/data.py`. Detect `__r2py_model__` on both sides and
route to a `_compare_model_fingerprint()` helper. I would keep this **inside the existing
DATA dimension** rather than adding a new effect dimension: it slots into the current
per-variable score without changing the score schema or `active_dims`, so score reports stay
shape-compatible with everything already built.

## Staging, starting with instrumentation

**Phase 0 — find out what the objects actually are (do this first, it's tiny).**
We know 1,278 exclusions and 75 variable *names*, but not one of their *types*. The warning
should log the R class and the Python type:

```
[r2py] WARNING: 'glmModel' excluded — R class c("glm","lm"), Python type statsmodels...GLMResultsWrapper
```

That turns guesswork into a ranked adapter worklist. Without it we would be writing adapters
for families we merely assume are common.

**Phase 1** — `linear_model` + `glm`. Judging by the names (`glmModel`, `model`, `irisFit*`,
`fit*`) this is the bulk of the 1,278.
**Phase 2** — `roc`, `clustering`, `preprocessor`.
**Phase 3** — the long tail, driven by the Phase 0 ranking.
**Always** — if either side has no adapter, fall back to today's exclusion, but record the
reason so adapter coverage is measurable over time.

## The caveat that matters most

This will **lower** measured scores, probably substantially. Those entities are currently
excluded, so a wrong model translation costs nothing today; once compared, it will score near
zero. Expect the `stats_objects` stratum to drop.

That is the point — it is a **validity fix, not a score improvement**. It converts a silent
blind spot into measured failure. But it means:

- the benchmark gets harder, and scores before/after this change are not comparable;
- it could *reduce* the apparent library effect, since the library has little to say about
  fitted-model equivalence;
- it must be pre-registered as a change, not slipped in, and ideally landed **after** the
  current experiment is fully analysed.

## Cheaper partial alternative

If the full fingerprint is too much work to justify now, there is a much smaller step with
most of the honesty benefit: **stop scoring excluded entities as absent and start reporting
them as a coverage statistic**. Add the count of excluded entities per script to the score
report and to `analyze`, so any claim about the corpus comes with "N% of data entities were
not comparable". That costs a few lines and removes the silent part of the problem without
changing any score.
