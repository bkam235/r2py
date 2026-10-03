---
id: timedate.degermanunity
package: timeDate
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# timedate.degermanunity

## Guidance
Translate R `DEGermanUnity` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "269241e4", "r_snippet": "DEGermanUnity(getRmetricsOptions(\"currentYear\"))", "py_snippet": "def DEGermanUnity(year=None, value=\"timeDate\", na_drop=True):\n    if year is None:\n        year = getRmetricsOptions(\"currentYear\")\n    \n    years = np.atleast_1d(year)\n    ans = []\n    for y in years:\n        # German Unity Day is October 3rd\n        ans.append(datetime.date(y, 10, 3))\n    \n    if value == \"timeDate\":\n        return [d.strftime(\"%Y-%m-%d\") for d in ans] if not np.isscalar(year) else ans[0].strftime(\"%Y-%m-%d\")\n    return ans\n\n# Execution\n\nprint(DEGermanUnity(getRmetricsOptions(\"currentYear\")))", "score": 0.9167, "script_id": "timeDate__rd_example__holiday-Dates_Rd", "n_calls": 0}

## Edit Examples
(none)
