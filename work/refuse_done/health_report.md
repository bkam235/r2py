# Health report: `work/refuse_done`

- Valid runs 50, invalid or failed 0; scorer version(s): `36a93ea5bd69-db31b28ade02` (50)
- Cost $3.64 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_rd | 50 | 0.502 | 0.768 | 0.80 | 0.24 | 50/50 | 19.4 | stalled 163, threshold 17 | 39 | 792 |

## Score gap (1 - mean final = 0.232)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 10 | 0.085 | 0.000 | 0.085 | 37% |
| improved, final < 0.9 | 28 | 0.104 | 0.032 | 0.136 | 58% |
| final >= 0.9 | 12 | 0.010 | 0.001 | 0.011 | 5% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `shiny__rd_example__updateRadioButtons_Rd` 0.030 (never improved), `pROC__rd_example__coords_Rd` 0.017 (never improved), `rvest__vignette__rvest_s7` 0.016 (never improved), `caret__rd_example__update_train_Rd` 0.015 (improved, final < 0.9), `reshape2__rd_example__melt_data_frame_Rd` 0.015 (improved, final < 0.9), `openssl__rd_example__ec_dh_Rd` 0.013 (improved, final < 0.9), `bslib__rd_example__value_box_Rd` 0.013 (improved, final < 0.9), `textshaping__rd_example__shape_text_Rd` 0.013 (never improved), `broom__rd_example__augment_felm_Rd` 0.012 (improved, final < 0.9), `systemfonts__rd_example__shape_string_Rd` 0.012 (never improved)

## Attribution

- Verifications 833: sentinels read 678, restored 55, **model mapping 100** (12%), mapping failed 0.

## Crashes

- Crashing candidates by exception: AttributeError 168, ValueError 106, TypeError 54, NameError 38, IndexError 12, KeyError 11, unclassified 8, ModuleNotFoundError 4, PatsyError 4, InvalidParameterError 2
- Runs ending with a crashing program (0): none

## Never-improving states (4 of 25)

- `rvest__vignette__rvest_s7`: start 0.592, start runs, 2 run(s)
- `shiny__rd_example__updateRadioButtons_Rd`: start 0.250, start runs, 2 run(s)
- `systemfonts__rd_example__shape_string_Rd`: start 0.709, start runs, 2 run(s)
- `textshaping__rd_example__shape_text_Rd`: start 0.678, start runs, 2 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 2 of 40 (5%). The check over-flags print labels and class names; read the examples.
  - `caret__rd_example__update_train_Rd` (default_2026_11_01_rd): ['Pre-processing: centered (4), scaled (4)', 'Resampling results across tuning parameters:', '#Neighbors', 'Accuracy']
  - `caret__rd_example__update_train_Rd` (default_2026_11_01_rd): ['Resampling results across tuning parameters:', 'Resampling: Cross-Validated (10 fold)', 'Accuracy']
