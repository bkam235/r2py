---
id: timedate.chsechselaeuten
package: timeDate
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# timedate.chsechselaeuten

## Guidance
Translate R `CHSechselaeuten` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "64e6c463", "r_snippet": "CHSechselaeuten(2000:2010)", "py_snippet": "def _nth_of_nday(year, month, day_of_week, nth):\n    # R: .nth.of.nday(y, 4, 1, 3) -> 3rd Monday (1) of April (4)\n    # Python dateutil: MO(3) for 3rd Monday\n    first_of_month = datetime.date(year, month, 1)\n    # weekday 0=Monday in python\n    target_day = first_of_month + relativedelta(weekday=MO(nth))\n    # If the 1st is a Tuesday, MO(1) might jump to the next week. \n    # But if 1st is Monday, MO(1) is the 1st. \n    # dateutil's MO(nth) works correctly from the start of the month.\n    if target_day.month != month:\n        # This handles cases where the date might wrap, though rare for nth of month\n        pass\n    return target_day\n\ndef CHSechselaeuten(year=None, value=\"timeDate\", na_drop=True):\n    if year is None:\n        year = getRmetricsOptions(\"currentYear\")\n    \n    years = np.atleast_1d(year)\n    ans = []\n    for y in years:\n        # 3rd Monday of April\n        theDate = _nth_of_nday(y, 4, 0, 3)\n        # If 3rd Monday is Easter Monday (Easter Sunday + 1), move to 4th Monday\n        if theDate == Easter(y, shift=1):\n            theDate = _nth_of_nday(y, 4, 0, 4)\n        ans.append(theDate)\n    \n    if value == \"timeDate\":\n        return [d.strftime(\"%Y-%m-%d\") for d in ans] if not np.isscalar(year) else ans[0].strftime(\"%Y-%m-%d\")\n    return ans\n\nyears_range = np.arange(2000, 2011)\nprint(CHSechselaeuten(years_range))", "score": 0.9713, "script_id": "timeDate__rd_example__holiday-Dates_Rd", "n_calls": 0}

## Edit Examples
(none)
