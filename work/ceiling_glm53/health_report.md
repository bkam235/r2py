# Health report: `work/ceiling_glm53`

- Valid runs 60, invalid or failed 0; scorer version(s): `6a9611f2ee76-db31b28ade02` (60)
- Cost $8.99 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_glm53_r8k | 60 | 0.508 | 0.861 | 0.73 | 0.58 | 60/60 | 12.1 | threshold 112, stalled 91, done 13 | 9 | 532 |

## Score gap (1 - mean final = 0.139)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 12 | 0.075 | 0.000 | 0.075 | 54% |
| improved, final < 0.9 | 13 | 0.036 | 0.014 | 0.050 | 36% |
| final >= 0.9 | 35 | 0.011 | 0.003 | 0.013 | 10% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `bslib__rd_example__page_fillable_Rd` 0.013 (never improved), `pROC__rd_example__coords_Rd` 0.010 (never improved), `ggplot2__rd_example__geom_bin_2d_Rd` 0.008 (never improved), `prodlim__rd_example__backGround_Rd` 0.008 (never improved), `openssl__rd_example__aes_cbc_Rd` 0.007 (never improved), `shape__rd_example__getellipse_Rd` 0.007 (improved, final < 0.9), `farver__rd_example__convert_colour_Rd` 0.006 (improved, final < 0.9), `openssl__rd_example__ec_dh_Rd` 0.005 (never improved), `textshaping__rd_example__shape_text_Rd` 0.005 (improved, final < 0.9), `systemfonts__rd_example__shape_string_Rd` 0.005 (never improved)

## Attribution

- Verifications 450: sentinels read 341, restored 19, **model mapping 90** (20%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 66, ValueError 44, IndexError 31, KeyError 28, AttributeError 22, NameError 20, RecursionError 2
- Runs ending with a crashing program (0): none

## Never-improving states (12 of 60)

- `bslib__rd_example__page_fillable_Rd`: start 0.250, start runs, 1 run(s)
- `farver__rd_example__as_white_ref_Rd`: start 0.821, start runs, 1 run(s)
- `ggplot2__rd_example__geom_bin_2d_Rd`: start 0.500, start runs, 1 run(s)
- `openssl__rd_example__aes_cbc_Rd`: start 0.550, start runs, 1 run(s)
- `openssl__rd_example__certificates_Rd`: start 0.741, start runs, 1 run(s)
- `openssl__rd_example__ec_dh_Rd`: start 0.670, start runs, 1 run(s)
- `pROC__rd_example__coords_Rd`: start 0.411, start runs, 1 run(s)
- `prodlim__rd_example__backGround_Rd`: start 0.500, start runs, 1 run(s)
- `proxy__rd_example__registry_Rd`: start 0.811, start runs, 1 run(s)
- `shape__rd_example__filledmultigonal_Rd`: start 0.750, start runs, 1 run(s)
- `systemfonts__rd_example__glyph_raster_Rd`: start 0.786, start runs, 1 run(s)
- `systemfonts__rd_example__shape_string_Rd`: start 0.709, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 3 of 44 (7%). The check over-flags print labels and class names; read the examples.
  - `caret__rd_example__update_train_Rd` (default_2026_11_01_glm53_r8k): ['Resampling results across tuning parameters:', 'Resampling: Cross-Validated (10 fold)', '#Neighbors', 'Accuracy']
  - `caret__vignette__caret_s3` (default_2026_11_01_glm53_r8k): ['..$ : chr "Resample1"']
  - `rvest__rd_example__html_table_Rd` (default_2026_11_01_glm53_r8k): ['xml_document', 'xml_node']
