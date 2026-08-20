---
id: timedate.easter
package: timeDate
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# timedate.easter

## Guidance
Translate R `Easter` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9ef3c8f2", "r_snippet": "Easter(2000:2005, -2) ", "py_snippet": "def Easter(year, shift=0):\n    years = np.atleast_1d(year)\n    # Computus algorithm for Gregorian Easter\n    a = years % 19\n    b = years // 100\n    c = years % 100\n    d = b // 4\n    e = b % 4\n    f = (b + 8) // 25\n    g = (b - f + 1) // 3\n    h = (19 * a + b - d - g + 15) % 30\n    i = c // 4\n    k = c % 4\n    l = (32 + 2 * e + 2 * i - h - k) % 7\n    m = (a + 11 * h + 22 * l) // 451\n    \n    month = (h + l - 7 * m + 114) // 31\n    day = ((h + l - 7 * m + 114) % 31) + 1\n    \n    dates = [datetime(int(y), int(m), int(d)) for y, m, d in zip(years, month, day)]\n    shifted_dates = [d + timedelta(", "score": 0.9851, "script_id": "auto"}

## Edit Examples
(none)
