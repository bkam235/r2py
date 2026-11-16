# Health report: `work/replay_default_e16`

- Valid runs 60, invalid or failed 0; scorer version(s): `6419ff591842-db31b28ade02` (60)
- Cost $1.99 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_12 | 60 | 0.514 | 0.909 | 0.87 | 0.75 | 60/60 | 16.5 | threshold 146, stalled 44, done 29 | 40 | 789 |

## Score gap (1 - mean final = 0.091)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 3 | 0.019 | 0.000 | 0.019 | 21% |
| improved, final < 0.9 | 12 | 0.046 | 0.004 | 0.051 | 56% |
| final >= 0.9 | 45 | 0.018 | 0.003 | 0.020 | 23% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `bslib__rd_example__page_fillable_Rd` 0.011 (improved, final < 0.9), `ggplot2__rd_example__geom_bin_2d_Rd` 0.008 (never improved), `openssl__rd_example__aes_cbc_Rd` 0.007 (never improved), `openssl__rd_example__ec_dh_Rd` 0.006 (improved, final < 0.9), `bslib__rd_example__value_box_Rd` 0.005 (improved, final < 0.9), `ragg__rd_example__agg_capture_Rd` 0.005 (improved, final < 0.9), `recipes__rd_example__step_kpca_Rd` 0.005 (improved, final < 0.9), `e1071__rd_example__boxplot_bclust_Rd` 0.004 (improved, final < 0.9), `caret__vignette__caret_s3` 0.004 (improved, final < 0.9), `systemfonts__rd_example__glyph_raster_Rd` 0.004 (never improved)

## Attribution

- Verifications 604: sentinels read 464, restored 39, **model mapping 101** (17%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 64, ValueError 45, AttributeError 40, KeyError 26, NameError 21, IndexError 15, PatsyError 6, unclassified 4
- Runs ending with a crashing program (0): none

## Never-improving states (3 of 60)

- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
    - `geom_bin_2d` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_1` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_2` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_3` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
    - `x` 0.25 (R, Py): [data] x: x: 'WAoAAAADAAQGAAADBQAAAAAFVVRGLTgAAAMTAAAABQAAAA4AAACWQBRmZmZmZmZAE5mZmZmZ\nmkASzMzMzMzNQBJmZmZmZmZAFAAAAAAAAEAVmZmZmZmaQBJmZmZmZmZAFAA; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
    - `x2` 0.25 (R, Py): [data] x2: x2: 'WAoAAAADAAQGAAADBQAAAAAFVVRGLTgAAAMTAAAABQAAAA4AAACWQBRmZmZmZmZAE5mZmZmZ\nmkASzMzMzMzNQBJmZmZmZmZAFAAAAAAAAEAVmZmZmZmaQBJmZmZmZmZAF; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
    - `y` 0.25 (R, Py): [data] y: y: type mismatch — R=str '/25ttYzah6bSD/SoRkBBfSSwXJjWpyRak9XbDho6HcphXym6K2eDzZJXFAW0NV7AcBN1NHf7\nqruySiF0RTUdORh2utqWEHVTDDK5Ew9wHrPsm; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
    - `R` 0.25 (R, Py): [data] R: R[0]: length 448 vs 150 — R=[[-603979776, -16777216, -16777216, -16777216, -16777216, -1610612736, 0, 0, -16777216, -16777216, -16777216,
    - `font` 0.89 (R, Py): [data] font: infra failure rescued by fallback (score 0.858): font: column sets differ — only_r=['lineheight', 'max_advance_height', 'underline_pos

## Pasting (deterministic check on changed final programs)

- Flagged 5 of 52 (10%). The check over-flags print labels and class names; read the examples.
  - `caret__rd_example__update_train_Rd` (default_2026_11_12): ['Pre-processing: centered (4), scaled (4)', 'Resampling results across tuning parameters:', '#Neighbors', 'Accuracy']
  - `caret__vignette__caret_s3` (default_2026_11_12): ['..$ : chr "Resample1"']
  - `proxy__rd_example__registry_Rd` (default_2026_11_12): ['* Distance measures:', 'variables. Biometrics, 26, pp. 525--534.']
  - `ranger__rd_example__csrf_Rd` (default_2026_11_12): ['versicolor', 'virginica']
  - `textshaping__rd_example__get_font_features_Rd` (default_2026_11_12): ['condensed', 'expanded']
