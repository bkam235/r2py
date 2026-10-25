# Health report: `work/replay_default`

- Valid runs 60, invalid or failed 0; scorer version(s): `unrecorded` (60)

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_10_20 | 60 | 0.415 | 0.782 | 0.75 | 0.37 | 59/60 | 18.5 | stalled 120, threshold 76, done 44 | 47 | 881 |

## Attribution

- Verifications 996: sentinels read 780, restored 83, **model mapping 133** (13%), mapping failed 0.

## Crashes

- Crashing candidates by exception: RuntimeError 216, AttributeError 168, truncated 141, TypeError 79, IndexError 42, NameError 40, TimeoutExpired 36, ValueError 22, SyntaxError 5, ModuleNotFoundError 3
- Runs ending with a crashing program (1): openssl__rd_example__certificates_Rd (default_2026_10_20 s0)

## Never-improving states (12 of 60)

- `bslib__rd_example__layout_column_wrap_Rd`: start 0.549, start runs, 1 run(s)
- `bslib__rd_example__page_fillable_Rd`: start 0.250, start runs, 1 run(s)
- `caret__vignette__caret_s3`: start 0.742, start runs, 1 run(s)
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
- `gtable__rd_example__gtable_add_cols_Rd`: start 0.700, start runs, 1 run(s)
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
- `openssl__rd_example__certificates_Rd`: start 0.000, start crashes, 1 run(s)
- `prodlim__rd_example__backGround_Rd`: start 0.500, start runs, 1 run(s)
- `shape__rd_example__filledmultigonal_Rd`: start 0.750, start runs, 1 run(s)
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
- `textshaping__rd_example__get_font_features_Rd`: start 0.739, start runs, 1 run(s)
- `textshaping__rd_example__shape_text_Rd`: start 0.678, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 4 of 45 (9%). The check over-flags print labels and class names; read the examples.
  - `caret__rd_example__update_train_Rd` (default_2026_10_20): ['Resampling results across tuning parameters:', 'Resampling: Cross-Validated (10 fold)', 'Accuracy', 'k-Nearest Neighbo
  - `rvest__rd_example__html_children_Rd` (default_2026_10_20): ['xml_document', 'xml_node']
  - `rvest__vignette__rvest_s7` (default_2026_10_20): ['xml_document', 'xml_node']
  - `recipes__rd_example__step_kpca_Rd` (default_2026_10_20): ['1 all_numeric_predictors() kpca_j6kS0']
