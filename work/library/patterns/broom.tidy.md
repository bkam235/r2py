---
id: broom.tidy
package: broom
confidence: tentative
seed: true
created: 2026-07-03
last_review: 2026-07-03
tie_count: 0
---

# broom.tidy

## Guidance
Translate R `tidy` (FunctionCall from broom) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "07865b96", "r_snippet": "    glance(dw)", "py_snippet": "def glance(x):\n    \"\"\"Mimics broom::glance for durbinWatsonTest output\"\"\"\n    return tidy(x)\n\n# Setup data\ndf = pd.DataFrame(mtcars)\n\nres_glance = glance(dw)\nprint(\"> glance(dw)\")\nprint(\"# A tibble: 1 × 5\")\nformatted_glance = res_glance.copy()\nformatted_glance['statistic'] = formatted_glance['statistic'].map(lambda x: f\"{x:.2f}\")\nformatted_glance['p.value'] = formatted_glance['p.value'].map(lambda x: f\"{x:.4f}\")\nformatted_glance['autocorrelation'] = formatted_glance['autocorrelation'].map(lambda x: f\"{x:.3f}\")\nprint(formatted_glance.to_string(index=False))", "score": 0.9336, "script_id": "auto"}
- {"r_hash": "64e70e0a", "r_snippet": "    tidy(dw)", "py_snippet": "def tidy(x):\n    \"\"\"Mimics broom::tidy for durbinWatsonTest output\"\"\"\n    return pd.DataFrame([x])\n\nres_tidy = tidy(dw)\nprint(\"> tidy(dw)\")\nprint(\"# A tibble: 1 × 5\")\n# Match R's output formatting: 2-3 decimal places\nformatted_tidy = res_tidy.copy()\nformatted_tidy['statistic'] = formatted_tidy['statistic'].map(lambda x: f\"{x:.2f}\")\nformatted_tidy['p.value'] = formatted_tidy['p.value'].map(lambda x: f\"{x:.4f}\")\nformatted_tidy['autocorrelation'] = formatted_tidy['autocorrelation'].map(lambda x: f\"{x:.3f}\")\nprint(formatted_tidy.to_string(index=False))", "score": 0.9326, "script_id": "auto"}

## Edit Examples
(none)
