# Health report: `work/feedback_e10`

- Valid runs 12, invalid or failed 0; scorer version(s): `06e4778f626b-db31b28ade02` (12)
- Cost $0.61 over 2 invocation(s); stop reasons: finished, finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_dsflash | 12 | 0.392 | 0.872 | 0.92 | 0.50 | 12/12 | 21.0 | threshold 23, stalled 14, done 8, budget 2 | 13 | 204 |

## Score gap (1 - mean final = 0.128)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 1 | 0.026 | 0.000 | 0.026 | 20% |
| improved, final < 0.9 | 5 | 0.059 | 0.025 | 0.084 | 66% |
| final >= 0.9 | 6 | 0.012 | 0.006 | 0.018 | 14% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `openssl__rd_example__ec_dh_Rd` 0.027 (improved, final < 0.9), `textshaping__rd_example__get_font_features_Rd` 0.026 (never improved), `recipes__rd_example__step_kpca_Rd` 0.023 (improved, final < 0.9), `shape__rd_example__Arrows_Rd` 0.014 (improved, final < 0.9), `isoband__vignette__isoband3_s2` 0.011 (improved, final < 0.9), `farver__rd_example__convert_colour_Rd` 0.009 (improved, final < 0.9), `lubridate__rd_example__period_Rd` 0.006 (final >= 0.9), `xml2__rd_example__xml_attr_Rd` 0.005 (final >= 0.9), `rvest__rd_example__html_element_Rd` 0.004 (final >= 0.9), `shiny__rd_example__updateRadioButtons_Rd` 0.003 (final >= 0.9)

## Attribution

- Verifications 160: sentinels read 108, restored 10, **model mapping 42** (26%), mapping failed 0.

## Crashes

- Crashing candidates by exception: ValueError 23, TypeError 20
- Runs ending with a crashing program (0): none

## Never-improving states (1 of 12)

- `textshaping__rd_example__get_font_features_Rd`: start 0.687, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 0 of 11 (0%). The check over-flags print labels and class names; read the examples.
