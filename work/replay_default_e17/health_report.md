# Health report: `work/replay_default_e17`

- Valid runs 60, invalid or failed 0; scorer version(s): `70026960c9df-45536fee3686` (60)
- Cost $2.35 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_21 | 60 | 0.516 | 0.924 | 0.88 | 0.77 | 60/60 | 19.4 | threshold 140, stalled 45, done 28 | 45 | 964 |

## Score gap (1 - mean final = 0.076)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 3 | 0.022 | 0.000 | 0.022 | 29% |
| improved, final < 0.9 | 11 | 0.038 | 0.004 | 0.042 | 55% |
| final >= 0.9 | 46 | 0.010 | 0.002 | 0.012 | 16% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `bslib__rd_example__page_fillable_Rd` 0.010 (never improved), `ggplot2__rd_example__geom_bin_2d_Rd` 0.008 (never improved), `ragg__rd_example__agg_capture_Rd` 0.007 (improved, final < 0.9), `openssl__rd_example__ec_dh_Rd` 0.005 (improved, final < 0.9), `recipes__rd_example__step_kpca_Rd` 0.005 (improved, final < 0.9), `isoband__vignette__isoband3_s2` 0.004 (improved, final < 0.9), `caret__vignette__caret_s3` 0.004 (improved, final < 0.9), `e1071__rd_example__boxplot_bclust_Rd` 0.004 (improved, final < 0.9), `systemfonts__rd_example__glyph_raster_Rd` 0.004 (never improved), `textshaping__rd_example__shape_text_Rd` 0.003 (improved, final < 0.9)

## Attribution

- Verifications 738: sentinels read 558, restored 65, **model mapping 115** (16%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 53, ValueError 32, NameError 29, KeyError 20, IndexError 17, AttributeError 17, TimeoutExpired 5, ModuleNotFoundError 4, UnboundLocalError 4, PatsyError 3
- Runs ending with a crashing program (0): none

## Never-improving states (3 of 60)

- `bslib__rd_example__page_fillable_Rd`: start 0.382, start runs, 1 run(s)
    - `ui` 0.38 (R, Py): [files] missing: ['tempfile:07d40e985ad7c747025dabb9f22142c4.woff2', 'tempfile:1f5e011d6aae0d98fc0518e1a303e99a.woff2', 'tempfile:1Ptug8zYS_SKggPNyC; [html] html_content_compared:1
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
    - `geom_bin_2d` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_1` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_2` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
    - `geom_bin_2d_3` 0.50 (R, Py): [graphics] figure count differs: R=1 Python=0; [warnings] warnings similarity 0.000 < 0.95
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
    - `R` 0.25 (R, Py): [data] R: R[0]: length 448 vs 150 — R=[[-603979776, -16777216, -16777216, -16777216, -16777216, -1610612736, 0, 0, -16777216, -16777216, -16777216,
    - `font` 0.89 (R, Py): [data] font: infra failure rescued by fallback (score 0.858): font: column sets differ — only_r=['lineheight', 'max_advance_height', 'underline_pos

## Pasting (deterministic check on changed final programs)

- Flagged 7 of 53 (13%). The check over-flags print labels and class names; read the examples.
  - `bslib__rd_example__value_box_Rd` (default_2026_11_21): ['<div class="card bslib-card bslib-mb-spacing html-fill-item html-fill-container bslib-value-box bg-success showcase-le
  - `caret__rd_example__update_train_Rd` (default_2026_11_21): ['Resampling results across tuning parameters:', 'Resampling: Cross-Validated (10 fold)', '#Neighbors', 'Accuracy']
  - `caret__vignette__caret_s3` (default_2026_11_21): ['..$ : chr "Resample1"']
  - `broom__rd_example__augment_felm_Rd` (default_2026_11_21): ['# ℹ Use `print(n = ...)` to see more rows']
  - `proxy__rd_example__registry_Rd` (default_2026_11_21): ['* Distance measures:', 'It is the proportion of (TRUE, TRUE) pairs, but not']
  - `sass__rd_example__sass_import_Rd` (default_2026_11_21): ['[1] "sass_file" "character"', 'attr(,"class")']
  - `textshaping__rd_example__get_font_features_Rd` (default_2026_11_21): ['condensed', 'expanded']
