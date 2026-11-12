# Health report: `work/smoke_glm53_r8k`

- Valid runs 1, invalid or failed 0; scorer version(s): `6a9611f2ee76-db31b28ade02` (1)
- Cost $0.03 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_glm53_r8k | 1 | 0.592 | 1.000 | 1.00 | 1.00 | 1/1 | 7.0 | threshold 3 | 0 | 4 |

## Score gap (1 - mean final = 0.000)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 0 | 0.000 | 0.000 | 0.000 | 0% |
| improved, final < 0.9 | 0 | 0.000 | 0.000 | 0.000 | 0% |
| final >= 0.9 | 1 | 0.000 | 0.000 | 0.000 | 0% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `rvest__vignette__rvest_s7` 0.000 (final >= 0.9)

## Attribution

- Verifications 7: sentinels read 7, restored 0, **model mapping 0** (0%), mapping failed 0.

## Crashes

- Crashing candidates by exception: AttributeError 4
- Runs ending with a crashing program (0): none

## Never-improving states (0 of 1)


## Pasting (deterministic check on changed final programs)

- Flagged 0 of 1 (0%). The check over-flags print labels and class names; read the examples.
