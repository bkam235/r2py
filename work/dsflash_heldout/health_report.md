# Health report: `work/dsflash_heldout`

- Valid runs 46, invalid or failed 0; scorer version(s): `6a9611f2ee76-db31b28ade02` (46)
- Cost $1.14 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_dsflash | 46 | 0.636 | 0.905 | 0.89 | 0.74 | 46/46 | 13.5 | threshold 85, stalled 37, done 20, budget 3 | 25 | 488 |

## Score gap (1 - mean final = 0.095)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 1 | 0.011 | 0.000 | 0.011 | 11% |
| improved, final < 0.9 | 11 | 0.061 | 0.011 | 0.072 | 76% |
| final >= 0.9 | 34 | 0.011 | 0.001 | 0.012 | 13% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `openssl__rd_example__keygen_Rd` 0.013 (improved, final < 0.9), `ggplot2__vignette__ggplot2-in-packages_s8` 0.011 (never improved), `ggplot2__rd_example__stat_summary_2d_Rd` 0.011 (improved, final < 0.9), `prodlim__rd_example__summary_prodlim_Rd` 0.010 (improved, final < 0.9), `e1071__rd_example__matchClasses_Rd` 0.008 (improved, final < 0.9), `textshaping__rd_example__plot_shape_Rd` 0.008 (improved, final < 0.9), `ranger__rd_example__hshrink_Rd` 0.008 (improved, final < 0.9), `ranger__rd_example__deforest_Rd` 0.004 (improved, final < 0.9), `clock__rd_example__time-point-rounding_Rd` 0.004 (improved, final < 0.9), `clock__rd_example__posixt-group_Rd` 0.003 (improved, final < 0.9)

## Attribution

- Verifications 400: sentinels read 351, restored 22, **model mapping 27** (7%), mapping failed 0.

## Crashes

- Crashing candidates by exception: NameError 18, AttributeError 15, ValueError 13, TypeError 12, LinAlgError 7, KeyError 6, ModuleNotFoundError 4, RuntimeError 4, IndexError 2, PlotnineError 2
- Runs ending with a crashing program (0): none

## Never-improving states (1 of 46)

- `ggplot2__vignette__ggplot2-in-packages_s8`: start 0.500, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 10 of 41 (24%). The check over-flags print labels and class names; read the examples.
  - `ModelMetrics__rd_example__logLoss_Rd` (default_2026_11_01_dsflash): ['[1] 0.1546854']
  - `clock__rd_example__iso-year-week-day-getters_Rd` (default_2026_11_01_dsflash): ['clock_calendar', 'clock_iso_year_week_day']
  - `broom__vignette__broom_chunk6` (default_2026_11_01_dsflash): ['# ℹ Use `print(n = ...)` to see more rows']
  - `clock__rd_example__time-point-rounding_Rd` (default_2026_11_01_dsflash): ['<naive_time<day>[2]>', '<naive_time<day>[41]>']
  - `caret__rd_example__modelLookup_Rd` (default_2026_11_01_dsflash): ['0.9, length = len), kappa = 0.5)', '1, alpha.pvals.expli = param$alpha.pvals.expli,']
  - `ggplot2__rd_example__stat_summary_2d_Rd` (default_2026_11_01_dsflash): ['ℹ The package "hexbin" is required for `stat_summary_hex()`.', '✖ Would you like to install it?']
  - `ranger__rd_example__deforest_Rd` (default_2026_11_01_dsflash): ['OOB prediction error (Brier s.):  NA', 'deforest.ranger']
  - `rmarkdown__rd_example__includes_Rd` (default_2026_11_01_dsflash): ['files_dir, output_dir)', 'function (...)']
  - `tidyr__vignette__pivot_s4` (default_2026_11_01_dsflash): ['# ℹ Use `print(n = ...)` to see more rows']
  - `textshaping__rd_example__plot_shape_Rd` (default_2026_11_01_dsflash): ['بـ جُل وحتى المتّبعة. حيث كنقطة الأهداف الأبرياء ثم, وبدأت إتفاقية الانجليزية جهة أي, كما الأجل الشتاء السيطرة أن. تم 
