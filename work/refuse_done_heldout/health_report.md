# Health report: `work/refuse_done_heldout`

- Valid runs 92, invalid or failed 0; scorer version(s): `36a93ea5bd69-db31b28ade02` (92)
- Cost $3.61 over 2 invocation(s); stop reasons: balance at the reserve: $0.42 left, finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_rd | 92 | 0.633 | 0.810 | 0.63 | 0.36 | 91/92 | 13.7 | stalled 230, threshold 69 | 50 | 977 |

## Score gap (1 - mean final = 0.190)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 27 | 0.082 | 0.000 | 0.082 | 43% |
| improved, final < 0.9 | 31 | 0.069 | 0.022 | 0.091 | 48% |
| final >= 0.9 | 33 | 0.007 | 0.000 | 0.007 | 4% |
| ends crashing | 1 | 0.000 | 0.011 | 0.011 | 6% |

States holding the most of the gap: `openssl__rd_example__keygen_Rd` 0.013 (improved, final < 0.9), `timechange__rd_example__time-zones_Rd` 0.011 (final >= 0.9), `ggplot2__vignette__ggplot2-in-packages_s8` 0.011 (never improved), `ggplot2__rd_example__stat_summary_2d_Rd` 0.011 (improved, final < 0.9), `broom__rd_example__augment_survreg_Rd` 0.011 (improved, final < 0.9), `prodlim__rd_example__summary_prodlim_Rd` 0.010 (never improved), `e1071__rd_example__matchClasses_Rd` 0.009 (never improved), `lubridate__rd_example__within-interval_Rd` 0.009 (never improved), `textshaping__rd_example__plot_shape_Rd` 0.008 (improved, final < 0.9), `farver__rd_example__compare_colour_Rd` 0.008 (never improved)

## Attribution

- Verifications 1150: sentinels read 964, restored 78, **model mapping 108** (9%), mapping failed 0.

## Crashes

- Crashing candidates by exception: AttributeError 186, KeyError 163, ValueError 73, NameError 60, TypeError 47, PlotnineError 22, IndexError 6, OverflowError 5, UnboundLocalError 5, UnknownTimeZoneError 5
- Runs ending with a crashing program (1): timechange__rd_example__time-zones_Rd (default_2026_11_01_rd s1)

## Never-improving states (11 of 46)

- `ModelMetrics__rd_example__logLoss_Rd`: start 0.838, start runs, 2 run(s)
- `ModelMetrics__rd_example__mse_Rd`: start 0.789, start runs, 2 run(s)
- `ModelMetrics__rd_example__rmse_Rd`: start 0.875, start runs, 2 run(s)
- `fansi__rd_example__strwrap_ctl_Rd`: start 0.736, start runs, 2 run(s)
- `farver__rd_example__compare_colour_Rd`: start 0.630, start runs, 2 run(s)
- `ggplot2__vignette__ggplot2-in-packages_s8`: start 0.500, start runs, 2 run(s)
- `gtable__rd_example__gtable_add_padding_Rd`: start 0.812, start runs, 2 run(s)
- `prodlim__rd_example__summary_prodlim_Rd`: start 0.536, start runs, 2 run(s)
- `ranger__rd_example__hshrink_Rd`: start 0.643, start runs, 2 run(s)
- `recipes__rd_example__step_YeoJohnson_Rd`: start 0.732, start runs, 2 run(s)
- `tidyr__rd_example__chop_Rd`: start 0.831, start runs, 2 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 10 of 59 (17%). The check over-flags print labels and class names; read the examples.
  - `clock__rd_example__iso-year-week-day-getters_Rd` (default_2026_11_01_rd): ['clock_calendar', 'clock_iso_year_week_day']
  - `clock__rd_example__time-point-rounding_Rd` (default_2026_11_01_rd): ['<naive_time<day>[2]>', '<naive_time<day>[41]>']
  - `gtable__rd_example__bind_Rd` (default_2026_11_01_rd): ['GRID.circle.2', 'GRID.lines.3']
  - `ggplot2__rd_example__stat_summary_2d_Rd` (default_2026_11_01_rd): ['ℹ The package "hexbin" is required for `stat_summary_hex()`.', '✖ Would you like to install it?']
  - `openssl__rd_example__keygen_Rd` (default_2026_11_01_rd): ['[2048-bit rsa private key]']
  - `textshaping__rd_example__plot_shape_Rd` (default_2026_11_01_rd): ['بـ جُل وحتى المتّبعة. حيث كنقطة الأهداف الأبرياء ثم, وبدأت إتفاقية الانجليزية جهة أي, كما الأجل الشتاء السيطرة أن. تم 
  - `clock__rd_example__time-point-rounding_Rd` (default_2026_11_01_rd): ['<naive_time<day>[2]>', '<naive_time<day>[41]>']
  - `ggplot2__rd_example__stat_summary_2d_Rd` (default_2026_11_01_rd): ['ℹ The package "hexbin" is required for `stat_summary_hex()`.', '✖ Would you like to install it?']
  - `textshaping__rd_example__plot_shape_Rd` (default_2026_11_01_rd): ['بـ جُل وحتى المتّبعة. حيث كنقطة الأهداف الأبرياء ثم, وبدأت إتفاقية الانجليزية جهة أي, كما الأجل الشتاء السيطرة أن. تم 
  - `tidyr__vignette__pivot_s4` (default_2026_11_01_rd): ['# A tibble: 180 × 3', '# ℹ 170 more rows']
