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
- {"r_hash": "07865b96", "r_snippet": "    glance(dw)", "py_snippet": "def glance(x):\n    \"\"\"Mimics broom::glance for durbinWatsonTest\"\"\"\n    return tidy(x)\n\nprint(\"> library(car)\")\n\nprint(\"> glance(dw)\")\nresult_glance = glance(dw)\nprint(\"# A tibble: 1 \\u00d7 5\")\nprint(result_glance.to_string(index=False))", "score": 0.9261, "script_id": "human-verified"}
- {"r_hash": "64e70e0a", "r_snippet": "    tidy(dw)", "py_snippet": "def tidy(x):\n    \"\"\"Mimics broom::tidy for durbinWatsonTest\"\"\"\n    if isinstance(x, dict) and \"dw\" in x:\n        return pd.DataFrame([{\n            \"statistic\": x[\"dw\"],\n            \"p.value\": x[\"p\"] if \"p\" in x else np.nan,\n            \"autocorrelation\": x[\"r\"],\n            \"method\": \"Durbin-Watson Test\",\n            \"alternative\": x[\"alternative\"]\n        }])\n    raise TypeError(\"No tidy method for this object type\")\n\nprint(\"> tidy(dw)\")\nresult_tidy = tidy(dw)\nprint(\"# A tibble: 1 \\u00d7 5\")\nprint(result_tidy.to_string(index=False))\nprint()\n\n# Same output for all durbinWatsonTests", "score": 0.9251, "script_id": "human-verified"}

## Edit Examples
(none)
