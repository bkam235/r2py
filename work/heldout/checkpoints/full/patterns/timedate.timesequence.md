---
id: timedate.timesequence
package: timeDate
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# timedate.timesequence

## Guidance
Translate R `timeSequence` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "522aeb7c", "r_snippet": "timeSequence(from = \"2004-03-26 05:00:00\", to = \"2004-04-02 05:00:00\",\n             zone = \"Europe/Zurich\", FinCenter = \"Europe/Zurich\")", "py_snippet": "res_ts = time_sequence(from_val=\"2004-03-26 05:00:00\", to_val=\"2004-04-02 05:00:00\", \n                    zone=\"Europe/Zurich\", fin_center=\"Europe/Zurich\")\nprint_r_style(res_ts, \"Europe/Zurich\")\n\n# ensure fixed clock time:", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-Sequence_Rd", "n_calls": 0}

## Edit Examples
(none)
