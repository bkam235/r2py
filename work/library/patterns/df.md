---
id: df
package: 
confidence: tentative
seed: true
created: 2026-06-05
last_review: 2026-06-10
tie_count: 4
---

# df

## Guidance
Translate R `df` (Variable from base R) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
- 021894dec169/: score regressed to 0.864
- dd2e0ea0b08b/: score regressed to 0.000
- dd2e0ea0b08b/: score regressed to 0.000
- d42c7e223bcd/: score regressed to 0.000

## Translation Examples
- {"r_hash": "6fccb871", "r_snippet": "df <- data.frame(\n  stringsAsFactors = FALSE,\n  date = as.Date(c(\"2019-01-01\", \"2019-02-01\")),\n  value = c(1, 2)\n)", "py_snippet": "df = pd.DataFrame({\n    'date': pd.to_datetime(['2019-01-01', '2019-02-01']),\n    'value': [1, 2]\n})", "score": 1.0, "script_id": "human-verified"}
- {"r_hash": "c301d570", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"es_ES\"), code = plot(df$date, df$value))", "py_snippet": "def with_locale(new, func):\n    \"\"\"\n    Temporarily set locale(s) and execute func, then restore original locale.\n    \n    Args:\n        new: dict mapping locale category strings to locale names\n        func: a callable or expression to execute under the new locale\n    \n    Returns:\n        The return value of func (if callable) or None\n    \"\"\"\n    \n    # Save original locales\n    original_locales = {}\n    for category in new.keys():\n        try:\n            original_locales[category] = locale.getlocale(getattr(locale, category))\n        except (AttributeError, ValueError):\n            origina", "score": 1.0, "script_id": "021894dec169"}
- {"r_hash": "e94e70f7", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"en_GB\"), format(ISOdate(2000, 1:12, 1), \"%B\"))", "py_snippet": "with_locale(new={\"LC_TIME\": \"en_GB\"}, func=lambda: [format(datetime.date(2000, m, 1), \"%B\") for m in range(1, 13)])", "score": 1.0, "script_id": "021894dec169"}

## Edit Examples
(none)
