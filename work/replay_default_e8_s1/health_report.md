# Health report: `work/replay_default_e8_s1`

- Valid runs 46, invalid or failed 0; scorer version(s): `36a93ea5bd69-db31b28ade02` (46)
- Cost $1.41 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01 | 46 | 0.642 | 0.766 | 0.59 | 0.30 | 46/46 | 9.8 | stalled 80, threshold 33, done 25 | 23 | 324 |

## Score gap (1 - mean final = 0.234)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 15 | 0.129 | 0.000 | 0.129 | 55% |
| improved, final < 0.9 | 17 | 0.092 | 0.000 | 0.092 | 39% |
| final >= 0.9 | 14 | 0.013 | 0.000 | 0.013 | 5% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `bslib__rd_example__page_fillable_Rd` 0.016 (never improved), `shiny__rd_example__updateRadioButtons_Rd` 0.016 (never improved), `farver__rd_example__convert_colour_Rd` 0.012 (never improved), `ggplot2__rd_example__geom_bin_2d_Rd` 0.011 (never improved), `prodlim__rd_example__backGround_Rd` 0.011 (never improved), `openssl__rd_example__aes_cbc_Rd` 0.010 (never improved), `rvest__vignette__rvest_s7` 0.009 (never improved), `caret__rd_example__update_train_Rd` 0.008 (improved, final < 0.9), `rvest__rd_example__html_children_Rd` 0.008 (improved, final < 0.9), `reshape2__rd_example__melt_data_frame_Rd` 0.008 (improved, final < 0.9)

## Attribution

- Verifications 397: sentinels read 325, restored 41, **model mapping 31** (8%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 20, AttributeError 17, KeyError 9, ModuleNotFoundError 8, ValueError 8, CompileError 4, IndexError 4, TimeoutError 3, unclassified 1
- Runs ending with a crashing program (0): none

## Never-improving states (15 of 46)

- `bslib__rd_example__page_fillable_Rd`: start 0.250, start runs, 1 run(s)
- `caret__vignette__caret_s3`: start 0.742, start runs, 1 run(s)
- `farver__rd_example__convert_colour_Rd`: start 0.443, start runs, 1 run(s)
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
- `openssl__rd_example__certificates_Rd`: start 0.741, start runs, 1 run(s)
- `prodlim__rd_example__backGround_Rd`: start 0.500, start runs, 1 run(s)
- `rvest__vignette__rvest_s7`: start 0.592, start runs, 1 run(s)
- `sass__rd_example__as_sass_Rd`: start 0.867, start runs, 1 run(s)
- `shape__rd_example__filledmultigonal_Rd`: start 0.750, start runs, 1 run(s)
- `shiny__rd_example__updateRadioButtons_Rd`: start 0.250, start runs, 1 run(s)
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
- `systemfonts__rd_example__shape_string_Rd`: start 0.709, start runs, 1 run(s)
- `textshaping__rd_example__get_font_features_Rd`: start 0.687, start runs, 1 run(s)
- `textshaping__rd_example__shape_text_Rd`: start 0.678, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 2 of 28 (7%). The check over-flags print labels and class names; read the examples.
  - `caret__rd_example__update_train_Rd` (default_2026_11_01): ["3 classes: 'setosa', 'versicolor', 'virginica'", 'Pre-processing: centered (4), scaled (4)', '#Neighbors', 'Accuracy']
  - `recipes__rd_example__step_kpca_Rd` (default_2026_11_01): ['1 all_numeric_predictors() kpca_j6kS0']
