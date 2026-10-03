---
id: base.identical
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.identical

## Guidance
Translate R `identical` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dc2be2c9", "r_snippet": "stopifnot( ## different formats even:\n  identical(t1, timeSequence(from = \"2004-03-12\", to = \"11-Apr-2004\")),\n  identical(t1, ## explicit format and FinCenter :\n      timeSequence(from = \"2004-03-12\", to = \"2004-04-11\",\n                   format = \"%Y-%m-%d\", FinCenter = \"GMT\")))", "py_snippet": "assert np.array_equal(t1, time_sequence(from_val=\"2004-03-12\", to_val=\"11-Apr-2004\"))\nassert np.array_equal(t1, time_sequence(from_val=\"2004-03-12\", to_val=\"2004-04-11\", \n                                        format_val=\"%Y-%m-%d\", fin_center=\"GMT\"))\n\n# observe \"switch to summer time\":", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-Sequence_Rd", "n_calls": 2}

## Edit Examples
(none)
