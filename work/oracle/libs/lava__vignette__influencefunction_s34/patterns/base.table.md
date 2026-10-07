---
id: base.table
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.table

## Guidance
Translate R `table` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e9953c79", "r_snippet": "tab <- table(g1, g2)", "py_snippet": "k_idx = np.array(k) - 1", "score": 1.0, "script_id": "e1071__rd_example__matchClasses_Rd.R", "n_calls": 1}
- {"r_hash": "99256250", "r_snippet": "with(aSAH, table(gender, outcome))", "py_snippet": "ct1 = pd.crosstab(aSAH['gender'], aSAH['outcome'])\nct1 = ct1.reindex(index=['Male', 'Female'], columns=['Good', 'Poor'])\nprint(\"      outcome\")\nprint(\"gender   Good Poor\")\nfor idx, row in ct1.iterrows():\n    print(f\"  {idx:<6} {row['Good']:>4} {row['Poor']:>4}\")\n\n# Age", "score": 1.0, "script_id": "pROC__rd_example__aSAH_Rd.R", "n_calls": 2}

## Edit Examples
(none)
