# Health report: `work/replay_default_e8`

- Valid runs 60, invalid or failed 0; scorer version(s): `36a93ea5bd69-db31b28ade02` (60)
- Cost $3.76 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01 | 60 | 0.492 | 0.809 | 0.73 | 0.38 | 60/60 | 15.8 | stalled 111, threshold 73, done 38 | 49 | 738 |

## Score gap (1 - mean final = 0.191)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 12 | 0.072 | 0.000 | 0.072 | 38% |
| improved, final < 0.9 | 25 | 0.079 | 0.030 | 0.109 | 57% |
| final >= 0.9 | 23 | 0.009 | 0.000 | 0.009 | 5% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `bslib__rd_example__page_fillable_Rd` 0.013 (never improved), `ggplot2__rd_example__geom_bin_2d_Rd` 0.008 (never improved), `prodlim__rd_example__backGround_Rd` 0.008 (never improved), `openssl__rd_example__aes_cbc_Rd` 0.007 (never improved), `shape__rd_example__getellipse_Rd` 0.007 (improved, final < 0.9), `rvest__vignette__rvest_s7` 0.007 (never improved), `caret__rd_example__update_train_Rd` 0.006 (improved, final < 0.9), `rvest__rd_example__html_children_Rd` 0.006 (improved, final < 0.9), `reshape2__rd_example__melt_data_frame_Rd` 0.006 (improved, final < 0.9), `farver__rd_example__convert_colour_Rd` 0.006 (improved, final < 0.9)

## Attribution

- Verifications 853: sentinels read 650, restored 69, **model mapping 134** (16%), mapping failed 0.

## Crashes

- Crashing candidates by exception: AttributeError 126, TypeError 91, ValueError 64, KeyError 31, NameError 24, IndexError 22, SyntaxError 3, FileNotFoundError 2, TimeoutExpired 2, DateParseError 2
- Runs ending with a crashing program (0): none

## Never-improving states (12 of 60)

- `bslib__rd_example__page_fillable_Rd`: start 0.250, start runs, 1 run(s)
    - `ui` 0.25 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
- `caret__vignette__caret_s3`: start 0.742, start runs, 1 run(s)
    - `inTrain` 0.25 (R, Py): [data] inTrain: infra failure rescued by fallback (score 0.027): inTrain: type mismatch — R=list [[1], [2], [3], [4], [5], [7], [10], [11], [12], [
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
    - `geom_bin_2d` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_1` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_2` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_3` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
    - `x` 0.25 (R, Py): [data] x: x: 'WAoAAAADAAQGAAADBQAAAAAFVVRGLTgAAAMTAAAABQAAAA4AAACWQBRmZmZmZmZAE5mZmZmZ\nmkASzMzMzMzNQBJmZmZmZmZAFAAAAAAAAEAVmZmZmZmaQBJmZmZmZmZAFAA; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
    - `x2` 0.25 (R, Py): [data] x2: x2: 'WAoAAAADAAQGAAADBQAAAAAFVVRGLTgAAAMTAAAABQAAAA4AAACWQBRmZmZmZmZAE5mZmZmZ\nmkASzMzMzMzNQBJmZmZmZmZAFAAAAAAAAEAVmZmZmZmaQBJmZmZmZmZAF; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
    - `y` 0.25 (R, Py): [data] y: y: type mismatch — R=str '/25ttYzah6bSD/SoRkBBfSSwXJjWpyRak9XbDho6HcphXym6K2eDzZJXFAW0NV7AcBN1NHf7\nqruySiF0RTUdORh2utqWEHVTDDK5Ew9wHrPsm; [data] iris: infra failure rescued by fallback (score 0.664): iris: column sets differ — only_r=[] only_py=['species'] — R={'Sepal.Length': [5.1, 4
- `openssl__rd_example__certificates_Rd`: start 0.741, start runs, 1 run(s)
    - `cert_data` 0.25 (R, Py): [data] all variables uncomparable: ['cert_data', 'chain']
    - `chain` 0.25 (R, Py): [data] all variables uncomparable: ['cert_data', 'chain']
    - `print_1` 0.72 (R, Py): [data] all variables uncomparable: ['cert_data', 'chain']
- `prodlim__rd_example__backGround_Rd`: start 0.500, start runs, 1 run(s)
    - `plot` 0.50 (R, Py): [graphics] plotted content similarity 0.000 < 0.99
    - `plot_1` 0.50 (R, Py): [graphics] plotted content similarity 0.000 < 0.99
- `rvest__vignette__rvest_s7`: start 0.592, start runs, 1 run(s)
    - `html_elements` 0.36 (no R bundle, Py): no message
    - `html` 0.42 (R, Py): [data] html: html: text forms differ (similarity 0.69) - R '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html
- `sass__rd_example__as_sass_Rd`: start 0.868, start runs, 1 run(s)
    - `input` 0.25 (R, Py): [files] missing: ['tempfile:variables5e00e5c1d6a']
    - `input_1` 0.95 (R, Py): [files] missing: ['tempfile:variables5e00e5c1d6a']; [data] input: input: '$color: blue
- `shape__rd_example__filledmultigonal_Rd`: start 0.750, start runs, 1 run(s)
    - `emptyplot` 0.75 (R, Py): [graphics] plotted content similarity 0.500 < 0.99
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
    - `R` 0.25 (R, Py): [data] R: R[0]: length 448 vs 150 — R=[[-603979776, -16777216, -16777216, -16777216, -16777216, -1610612736, 0, 0, -16777216, -16777216, -16777216,
    - `font` 0.89 (R, Py): [data] font: infra failure rescued by fallback (score 0.858): font: column sets differ — only_r=['lineheight', 'max_advance_height', 'underline_pos
- `systemfonts__rd_example__shape_string_Rd`: start 0.709, start runs, 1 run(s)
    - `shape_string` 0.56 (R, Py): no message
    - `shape_string_1` 0.57 (R, Py): no message
- `textshaping__rd_example__shape_text_Rd`: start 0.678, start runs, 1 run(s)
    - `shape_text` 0.52 (R, Py): no message
    - `shape_text_1` 0.52 (R, Py): no message

## Pasting (deterministic check on changed final programs)

- Flagged 3 of 44 (7%). The check over-flags print labels and class names; read the examples.
  - `farver__rd_example__as_white_ref_Rd` (default_2026_11_01): ['X         Y         Z']
  - `caret__rd_example__update_train_Rd` (default_2026_11_01): ['Resampling results across tuning parameters:', 'Summary of sample sizes: 135, 135, 135, 135, 135, 135, ...', 'Accuracy
  - `recipes__rd_example__step_kpca_Rd` (default_2026_11_01): ['1 all_numeric_predictors() kpca_j6kS0']
