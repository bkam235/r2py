# Health report: `work/smoke_dsflash`

- Valid runs 2, invalid or failed 0; scorer version(s): `6a9611f2ee76-db31b28ade02` (2)
- Cost $0.08 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_dsflash | 2 | 0.339 | 0.986 | 1.00 | 1.00 | 2/2 | 26.5 | threshold 9 | 1 | 44 |

## Score gap (1 - mean final = 0.015)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 0 | 0.000 | 0.000 | 0.000 | 0% |
| improved, final < 0.9 | 0 | 0.000 | 0.000 | 0.000 | 0% |
| final >= 0.9 | 2 | 0.015 | 0.000 | 0.015 | 100% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `textshaping__rd_example__shape_text_Rd` 0.015 (final >= 0.9), `lava__rd_example__csplit_Rd` 0.000 (final >= 0.9)

## Attribution

- Verifications 34: sentinels read 33, restored 0, **model mapping 1** (3%), mapping failed 0.

## Crashes

- Crashing candidates by exception: TypeError 10
- Runs ending with a crashing program (0): none

## Never-improving states (0 of 2)


## Pasting (deterministic check on changed final programs)

- Flagged 0 of 2 (0%). The check over-flags print labels and class names; read the examples.
