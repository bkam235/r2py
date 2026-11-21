# Health report: `work/replay_default_e17_heldout`

- Valid runs 46, invalid or failed 0; scorer version(s): `70026960c9df-45536fee3686` (46)
- Cost $1.24 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_21 | 46 | 0.640 | 0.915 | 0.89 | 0.76 | 46/46 | 14.6 | threshold 93, stalled 36, done 19 | 18 | 531 |

## Score gap (1 - mean final = 0.085)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 2 | 0.016 | 0.000 | 0.016 | 19% |
| improved, final < 0.9 | 9 | 0.057 | 0.006 | 0.063 | 74% |
| final >= 0.9 | 35 | 0.005 | 0.000 | 0.005 | 6% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `openssl__rd_example__keygen_Rd` 0.013 (improved, final < 0.9), `ggplot2__vignette__ggplot2-in-packages_s8` 0.011 (never improved), `prodlim__rd_example__summary_prodlim_Rd` 0.009 (improved, final < 0.9), `e1071__rd_example__matchClasses_Rd` 0.008 (improved, final < 0.9), `textshaping__rd_example__plot_shape_Rd` 0.008 (improved, final < 0.9), `ranger__rd_example__hshrink_Rd` 0.008 (improved, final < 0.9), `ggplot2__rd_example__stat_summary_2d_Rd` 0.006 (improved, final < 0.9), `rmarkdown__rd_example__includes_Rd` 0.005 (never improved), `caret__rd_example__modelLookup_Rd` 0.005 (improved, final < 0.9), `ranger__rd_example__deforest_Rd` 0.004 (improved, final < 0.9)

## Attribution

- Verifications 463: sentinels read 382, restored 21, **model mapping 60** (13%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 22, AttributeError 19, KeyError 11, ValueError 10, PlotnineError 8, NameError 5, RuntimeError 4, TimeoutExpired 4, unclassified 4, LinAlgError 2
- Runs ending with a crashing program (0): none

## Never-improving states (2 of 46)

- `ggplot2__vignette__ggplot2-in-packages_s8`: start 0.500, start runs, 1 run(s)
    - `col_summary_1` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0
- `rmarkdown__rd_example__includes_Rd`: start 0.750, start runs, 1 run(s)
    - `pdf_document` 0.50 (R, Py): [stdout] R auto-prints this expression's result to stdout, but Python produces no output for this entity. Change the Python code or append to it so t

## Pasting (deterministic check on changed final programs)

- Flagged 8 of 41 (20%). The check over-flags print labels and class names; read the examples.
  - `broom__vignette__broom_chunk6` (default_2026_11_21): ['# ℹ Use `print(n = ...)` to see more rows']
  - `clock__rd_example__time-point-rounding_Rd` (default_2026_11_21): ['2147483648.0', 'clock_naive_time', 'clock_rcrd']
  - `ggplot2__rd_example__stat_summary_2d_Rd` (default_2026_11_21): ['ℹ The package "hexbin" is required for `stat_summary_hex()`.', '✖ Would you like to install it?']
  - `caret__rd_example__modelLookup_Rd` (default_2026_11_21): ['dat <- if (is.data.frame(x))', 'dat$.outcome <- y']
  - `broom__rd_example__augment_survreg_Rd` (default_2026_11_21): ['# ℹ Use `print(n = ...)` to see more rows', '(Intercept)']
  - `tidyr__vignette__pivot_s4` (default_2026_11_21): ['# ℹ Use `print(n = ...)` to see more rows']
  - `textshaping__rd_example__plot_shape_Rd` (default_2026_11_21): ['بـ جُل وحتى المتّبعة. حيث كنقطة الأهداف الأبرياء ثم, وبدأت إتفاقية الانجليزية جهة أي, كما الأجل الشتاء السيطرة أن. تم 
  - `timechange__rd_example__time-zones_Rd` (default_2026_11_21): ['Time differences in hours', 'Time differences in secs']
