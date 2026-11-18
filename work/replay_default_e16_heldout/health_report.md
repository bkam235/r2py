# Health report: `work/replay_default_e16_heldout`

- Valid runs 46, invalid or failed 0; scorer version(s): `6419ff591842-db31b28ade02` (46)
- Cost $1.07 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_12 | 46 | 0.640 | 0.902 | 0.89 | 0.72 | 46/46 | 12.6 | threshold 96, stalled 30, done 22 | 24 | 442 |

## Score gap (1 - mean final = 0.098)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 1 | 0.011 | 0.000 | 0.011 | 11% |
| improved, final < 0.9 | 12 | 0.068 | 0.006 | 0.074 | 76% |
| final >= 0.9 | 33 | 0.011 | 0.001 | 0.013 | 13% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `openssl__rd_example__keygen_Rd` 0.013 (improved, final < 0.9), `ggplot2__vignette__ggplot2-in-packages_s8` 0.011 (never improved), `prodlim__rd_example__summary_prodlim_Rd` 0.010 (improved, final < 0.9), `e1071__rd_example__matchClasses_Rd` 0.008 (improved, final < 0.9), `textshaping__rd_example__plot_shape_Rd` 0.008 (improved, final < 0.9), `ranger__rd_example__hshrink_Rd` 0.008 (improved, final < 0.9), `ggplot2__rd_example__stat_summary_2d_Rd` 0.006 (improved, final < 0.9), `farver__rd_example__native_encoding_Rd` 0.005 (improved, final < 0.9), `recipes__rd_example__step_YeoJohnson_Rd` 0.004 (improved, final < 0.9), `ranger__rd_example__deforest_Rd` 0.004 (improved, final < 0.9)

## Attribution

- Verifications 384: sentinels read 315, restored 27, **model mapping 42** (11%), mapping failed 0.

## Crashes

- Crashing candidates by exception: NameError 25, AttributeError 16, KeyError 7, TypeError 6, ValueError 3, ModuleNotFoundError 2, ImportError 2, PlotnineError 2, IndexError 2, UnboundLocalError 1
- Runs ending with a crashing program (0): none

## Never-improving states (1 of 46)

- `ggplot2__vignette__ggplot2-in-packages_s8`: start 0.500, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 5 of 41 (12%). The check over-flags print labels and class names; read the examples.
  - `clock__rd_example__time-point-rounding_Rd` (default_2026_11_12): ['2147483648.0', 'clock_naive_time', 'clock_rcrd']
  - `caret__rd_example__modelLookup_Rd` (default_2026_11_12): ['as.data.frame(out, stringsAsFactors = TRUE)', 'colnames(out) <- dimnames(modelCoef)[[2]]']
  - `ggplot2__rd_example__stat_summary_2d_Rd` (default_2026_11_12): ['ℹ The package "hexbin" is required for `stat_summary_hex()`.', '✖ Would you like to install it?']
  - `tidyr__vignette__pivot_s4` (default_2026_11_12): ['# ℹ Use `print(n = ...)` to see more rows']
  - `textshaping__rd_example__plot_shape_Rd` (default_2026_11_12): ['C:\\WINDOWS\\Fonts\\arial.ttf', 'بـ جُل وحتى المتّبعة. حيث كنقطة الأهداف الأبرياء ثم, وبدأت إتفاقية الانجليزية جهة أي,
