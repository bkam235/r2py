---
id: base.sample
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.sample

## Guidance
Translate R `sample` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "764eabed", "r_snippet": "k <- sample(1:1000, size=200)", "py_snippet": "print(*(m1))", "score": 1.0, "script_id": "e1071__rd_example__matchClasses_Rd.R", "n_calls": 1}
- {"r_hash": "22cd25e9", "r_snippet": "random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]", "py_snippet": "# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]\nrandom_idx = random.randint(0, len(sys_fonts) - 1)\nrandom_font = sys_fonts.iloc[random_idx]['family']", "score": 1.0, "script_id": "textshaping__rd_example__get_font_features_Rd.R", "n_calls": 2}

## Edit Examples
(none)
