---
id: timedate.holiday
package: timeDate
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# timedate.holiday

## Guidance
Translate R `holiday` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "295322af", "r_snippet": "holiday(2024:2025, Holiday = c(Easter), names = TRUE)", "py_snippet": "def holiday(year=None, Holiday=\"Easter\", names=False):\n    if year is None:\n        year = datetime.now().year\n    \n    years = np.atleast_1d(year)\n    \n    # Mimic R's substitute/all.names for naming\n    # This is a simplified version of the R logic\n    if isinstance(Holiday, str):\n        holiday_funcs = [_get_holiday_func(Holiday)]\n        holiday_names = [Holiday]\n    elif callable(Holiday):\n        holiday_funcs = [Holiday]\n        holiday_names = [Holiday.__name__]\n    elif isinstance(Holiday, (list, np.ndarray)):\n        holiday_funcs = [_get_holiday_func(h) if isinstance(h, str) else h", "score": 0.9138, "script_id": "auto"}

## Edit Examples
(none)
