---
id: timedate.goodfriday
package: timeDate
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# timedate.goodfriday

## Guidance
Translate R `GoodFriday` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8cccbf16", "r_snippet": "GoodFriday(2000:2005)", "py_snippet": "def GoodFriday(year, value=\"timeDate\", na_drop=True):\n    return Easter(year, -2)\n\ndef ChristmasDay(year, value=\"timeDate\", na_drop=True):\n    years = np.atleast_1d(year)\n    res = [f\"{int(y)}-12-25\" for y in years]\n    return np.array(res) if np.ndim(year) > 0 else res[0]\n\ndef GBEarlyMayBankHoliday(year, value=\"timeDate\", na_drop=True):\n    years = np.atleast_1d(year)\n    res = []\n    for y in years:\n        if y < 1978:\n            res.append(np.nan if not na_drop else None)\n            continue\n        \n        if y in [1995, 2020]:\n            res.append(f\"{int(y)}-05-08\")\n        else:\n  ", "score": 0.9851, "script_id": "auto"}

## Edit Examples
(none)
