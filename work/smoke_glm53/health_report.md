# Health report: `work/smoke_glm53`

- Valid runs 1, invalid or failed 0; scorer version(s): `6a9611f2ee76-db31b28ade02` (1)
- Cost $0.04 over 1 invocation(s); stop reasons: finished; sleep gaps: 0

## Arms

| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |
|---|---|---|---|---|---|---|---|---|---|---|
| default_2026_11_01_glm53 | 1 | 0.592 | 0.592 | 0.00 | 0.00 | 1/1 | 0.0 |  | 0 | 0 |

## Score gap (1 - mean final = 0.408)

Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up to the gap). Questions are worth what share of it they can reach.

| outcome | runs | start runs | start crashes | total | share |
|---|---|---|---|---|---|
| never improved | 1 | 0.408 | 0.000 | 0.408 | 100% |
| improved, final < 0.9 | 0 | 0.000 | 0.000 | 0.000 | 0% |
| final >= 0.9 | 0 | 0.000 | 0.000 | 0.000 | 0% |
| ends crashing | 0 | 0.000 | 0.000 | 0.000 | 0% |

States holding the most of the gap: `rvest__vignette__rvest_s7` 0.408 (never improved)

## Attribution

- No attribution statistics recorded.

## Crashes

- Crashing candidates by exception: none
- Runs ending with a crashing program (0): none

## Never-improving states (1 of 1)

- `rvest__vignette__rvest_s7`: start 0.592, start runs, 1 run(s)

(`--deep` re-verifies these starts and lists their losing entities.)

## Pasting (deterministic check on changed final programs)

- Flagged 0 of 0 (0%). The check over-flags print labels and class names; read the examples.
