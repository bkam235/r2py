# Health report: `work/replay_default`

- Valid runs 60, invalid or failed 0; scorer version(s): `unrecorded` (60)

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_10_20 | 60 | 0.415 | 0.782 | 0.75 | 0.37 | 59/60 | 18.5 | stalled 120, threshold 76, done 44 | 47 | 881 |

## Score gap (1 - mean final = 0.218)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 11 | 0.071 | 0.000 | 0.071 | 33% |
| improved, final < 0.9 | 26 | 0.081 | 0.037 | 0.118 | 54% |
| final >= 0.9 | 22 | 0.008 | 0.005 | 0.012 | 6% |
| ends crashing | 1 | 0.000 | 0.017 | 0.017 | 8% |

States holding the most of the gap: `openssl__rd_example__certificates_Rd` 0.017 (ends crashing), `bslib__rd_example__page_fillable_Rd` 0.013 (never improved), `e1071__rd_example__boxplot_bclust_Rd` 0.010 (improved, final < 0.9), `farver__rd_example__convert_colour_Rd` 0.009 (improved, final < 0.9), `ggplot2__rd_example__geom_bin_2d_Rd` 0.008 (never improved), `prodlim__rd_example__backGround_Rd` 0.008 (never improved), `bslib__rd_example__layout_column_wrap_Rd` 0.008 (never improved), `openssl__rd_example__aes_cbc_Rd` 0.007 (never improved), `shape__rd_example__getellipse_Rd` 0.007 (improved, final < 0.9), `caret__rd_example__update_train_Rd` 0.007 (improved, final < 0.9)

## Attribution

- Verifications 996: sentinels read 780, restored 83, **model mapping 133** (13%), mapping failed 0.

## Crashes

- Crashing candidates by exception: RuntimeError 216, AttributeError 168, truncated 141, TypeError 79, IndexError 42, NameError 40, TimeoutExpired 36, ValueError 22, SyntaxError 5, ModuleNotFoundError 3
- Runs ending with a crashing program (1): openssl__rd_example__certificates_Rd (default_2026_10_20 s0)

## Never-improving states (12 of 60)

- `bslib__rd_example__layout_column_wrap_Rd`: start 0.549, start runs, 1 run(s)
    - `layout_column_wrap` 0.50 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
    - `layout_column_wrap_1` 0.50 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
    - `layout_column_wrap_2` 0.50 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
    - `layout_column_wrap_3` 0.50 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
    - `x` 0.74 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
- `bslib__rd_example__page_fillable_Rd`: start 0.250, start runs, 1 run(s)
    - `ui` 0.25 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
- `caret__vignette__caret_s3`: start 0.742, start runs, 1 run(s)
    - `inTrain` 0.25 (R, Py): [data] inTrain: infra failure rescued by fallback (score 0.027): inTrain: type mismatch — R=list [[1], [2], [3], [4], [5], [7], [10], [11], [12], [
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
    - `geom_bin_2d` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_1` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_2` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_3` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
- `gtable__rd_example__gtable_add_cols_Rd`: start 0.700, start runs, 1 run(s)
    - `rect` 0.25 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] rect: missing in Python output (R={'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.re
    - `tab` 0.25 (R, no Py bundle): [warnings] warnings similarity 0.000 < 0.95
    - `tab2` 0.25 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] tab2: missing in Python output (R={'grobs': [{'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name
    - `tab3` 0.25 (R, no Py bundle): [warnings] warnings similarity 0.000 < 0.95
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
    - `x` 0.25 (R, Py): [data] x: x: 'WAoAAAADAAQGAAADBQAAAAAFVVRGLTgAAAMTAAAABQAAAA4AAACWQBRmZmZmZmZAE5mZmZmZ\nmkASzMzMzMzNQBJmZmZmZmZAFAAAAAAAAEAVmZmZmZmaQBJmZmZmZmZAFAA; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
    - `x2` 0.25 (R, Py): [data] x2: x2: 'WAoAAAADAAQGAAADBQAAAAAFVVRGLTgAAAMTAAAABQAAAA4AAACWQBRmZmZmZmZAE5mZmZmZ\nmkASzMzMzMzNQBJmZmZmZmZAFAAAAAAAAEAVmZmZmZmaQBJmZmZmZmZAF; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
    - `y` 0.25 (R, Py): [data] y: y: type mismatch — R=str '/25ttYzah6bSD/SoRkBBfSSwXJjWpyRak9XbDho6HcphXym6K2eDzZJXFAW0NV7AcBN1NHf7\nqruySiF0RTUdORh2utqWEHVTDDK5Ew9wHrPsm; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
- `openssl__rd_example__certificates_Rd`: start 0.000, start crashes, 1 run(s)
    - `cert_data` 0.25 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] all variables uncomparable: ['cert_data', 'chain']
    - `chain` 0.25 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] all variables uncomparable: ['cert_data', 'chain']
    - `print_1` 0.72 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] all variables uncomparable: ['cert_data', 'chain']
- `prodlim__rd_example__backGround_Rd`: start 0.500, start runs, 1 run(s)
    - `plot` 0.50 (R, Py): [graphics] plotted content similarity 0.000 < 0.99; [warnings] warnings similarity 0.000 < 0.95
    - `plot_1` 0.50 (R, Py): [graphics] plotted content similarity 0.000 < 0.99; [warnings] warnings similarity 0.000 < 0.95
- `shape__rd_example__filledmultigonal_Rd`: start 0.750, start runs, 1 run(s)
    - `emptyplot` 0.75 (R, Py): [graphics] plotted content similarity 0.500 < 0.99; [warnings] warnings similarity 0.000 < 0.95
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
    - `R` 0.25 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] R: R[0]: length 448 vs 150 — R=[[-603979776, -16777216, -16777216, -16777216, -16777216, -1610612736, 0, 0, -16777216, -16777216, -16777216,
    - `font` 0.89 (R, Py): [warnings] warnings similarity 0.000 < 0.95; [data] font: infra failure rescued by fallback (score 0.858): font: column sets differ — only_r=['lineheight', 'max_advance_height', 'underline_pos
- `textshaping__rd_example__get_font_features_Rd`: start 0.739, start runs, 1 run(s)
    - `sys_fonts` 0.32 (R, Py): [data] sys_fonts: infra failure rescued by fallback (score 0.096): sys_fonts: column sets differ — only_r=['name', 'variable', 'weight', 'width'] o; [rng] RNG sequence length mismatch: R=1 Python=0
    - `get_font_features` 0.74 (R, Py): [rng] RNG sequence length mismatch: R=1 Python=0
- `textshaping__rd_example__shape_text_Rd`: start 0.678, start runs, 1 run(s)
    - `shape_text` 0.52 (R, Py): no message
    - `shape_text_1` 0.52 (R, Py): no message

## Pasting (deterministic check on changed final programs)

- Flagged 4 of 45 (9%). The check over-flags print labels and class names; read the examples.
  - `caret__rd_example__update_train_Rd` (default_2026_10_20): ['Resampling results across tuning parameters:', 'Resampling: Cross-Validated (10 fold)', 'Accuracy', 'k-Nearest Neighbo
  - `rvest__rd_example__html_children_Rd` (default_2026_10_20): ['xml_document', 'xml_node']
  - `rvest__vignette__rvest_s7` (default_2026_10_20): ['xml_document', 'xml_node']
  - `recipes__rd_example__step_kpca_Rd` (default_2026_10_20): ['1 all_numeric_predictors() kpca_j6kS0']
