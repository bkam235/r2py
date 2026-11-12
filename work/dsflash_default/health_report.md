# Health report: `work/dsflash_default`

- Valid runs 60, invalid or failed 0; scorer version(s): `6a9611f2ee76-db31b28ade02` (60)
- Cost $2.06 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_dsflash | 60 | 0.508 | 0.883 | 0.82 | 0.68 | 60/60 | 17.1 | threshold 138, stalled 49, done 32, budget 1 | 29 | 817 |

## Score gap (1 - mean final = 0.117)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 7 | 0.057 | 0.000 | 0.057 | 49% |
| improved, final < 0.9 | 12 | 0.033 | 0.010 | 0.043 | 37% |
| final >= 0.9 | 41 | 0.014 | 0.003 | 0.017 | 15% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `bslib__rd_example__page_fillable_Rd` 0.013 (never improved), `shiny__rd_example__updateRadioButtons_Rd` 0.013 (never improved), `ggplot2__rd_example__geom_bin_2d_Rd` 0.008 (never improved), `prodlim__rd_example__backGround_Rd` 0.008 (never improved), `openssl__rd_example__aes_cbc_Rd` 0.007 (never improved), `openssl__rd_example__ec_dh_Rd` 0.005 (improved, final < 0.9), `farver__rd_example__convert_colour_Rd` 0.005 (improved, final < 0.9), `recipes__rd_example__step_kpca_Rd` 0.005 (improved, final < 0.9), `caret__vignette__caret_s3` 0.004 (improved, final < 0.9), `shape__rd_example__filledmultigonal_Rd` 0.004 (never improved)

## Attribution

- Verifications 629: sentinels read 494, restored 33, **model mapping 102** (16%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 62, ValueError 38, KeyError 23, AttributeError 22, IndexError 21, NameError 17, ModuleNotFoundError 2, FileNotFoundError 1
- Runs ending with a crashing program (0): none

## Never-improving states (7 of 60)

- `bslib__rd_example__page_fillable_Rd`: start 0.250, start runs, 1 run(s)
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
- `prodlim__rd_example__backGround_Rd`: start 0.500, start runs, 1 run(s)
- `shape__rd_example__filledmultigonal_Rd`: start 0.750, start runs, 1 run(s)
- `shiny__rd_example__updateRadioButtons_Rd`: start 0.250, start runs, 1 run(s)
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 8 of 49 (16%). The check over-flags print labels and class names; read the examples.
  - `bslib__rd_example__value_box_Rd` (default_2026_11_01_dsflash): ['<div class="card-body bslib-gap-spacing html-fill-item html-fill-container" style="margin-top:auto;margin-bottom:auto;
  - `caret__rd_example__update_train_Rd` (default_2026_11_01_dsflash): ['Resampling results across tuning parameters:', 'The tuning parameter was set manually.', '#Neighbors', 'Accuracy']
  - `caret__vignette__caret_s3` (default_2026_11_01_dsflash): ['..$ : chr "Resample1"']
  - `proxy__rd_example__registry_Rd` (default_2026_11_01_dsflash): ['* Distance measures:']
  - `reshape2__rd_example__parse_formula_Rd` (default_2026_11_01_dsflash): ['- attr(*, "env")=<environment: 0x000001e9a5e1b3b8>']
  - `rvest__rd_example__html_children_Rd` (default_2026_11_01_dsflash): ['xml_document', 'xml_node']
  - `rvest__rd_example__html_table_Rd` (default_2026_11_01_dsflash): ['xml_document', 'xml_node']
  - `textshaping__rd_example__get_font_features_Rd` (default_2026_11_01_dsflash): ['MS Sans Serif', 'MS Serif']
