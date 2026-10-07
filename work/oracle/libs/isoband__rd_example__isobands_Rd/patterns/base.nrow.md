---
id: base.nrow
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.nrow

## Guidance
Translate R `nrow` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cb24b082", "r_snippet": "  summarise(nrows = nrow(pick(everything())))", "py_snippet": "result = d.groupby('cyl').size().reset_index(name='nrows')", "score": 0.9667, "script_id": "dplyr__vignette__rowwise_s36.R", "n_calls": 1}
- {"r_hash": "22cd25e9", "r_snippet": "random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]", "py_snippet": "# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]\nrandom_idx = random.randint(0, len(sys_fonts) - 1)\nrandom_font = sys_fonts.iloc[random_idx]['family']", "score": 1.0, "script_id": "textshaping__rd_example__get_font_features_Rd.R", "n_calls": 2}

## Edit Examples
(none)
