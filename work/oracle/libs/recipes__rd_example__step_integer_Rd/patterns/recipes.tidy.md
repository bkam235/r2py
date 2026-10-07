---
id: recipes.tidy
package: recipes
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# recipes.tidy

## Guidance
Translate R `tidy` from recipes to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "981e5af8", "r_snippet": "tidy(yj_transform, number = 1)", "py_snippet": "# plot(density(yj_te$sulfur), main = \"after\")\nplt.figure()\nyj_te['sulfur'].plot(kind='kde')\nplt.title(\"after\")\n\n# tidy(yj_transform, number = 1)\ntidy_1 = pd.DataFrame({\n    'terms': ['all_numeric()'],", "score": 0.9699, "script_id": "recipes__rd_example__step_YeoJohnson_Rd.R", "n_calls": 0}

## Edit Examples
(none)
