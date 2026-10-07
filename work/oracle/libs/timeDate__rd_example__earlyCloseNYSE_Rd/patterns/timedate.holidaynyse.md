---
id: timedate.holidaynyse
package: timedate
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# timedate.holidaynyse

## Guidance
Translate R `holidaynyse` from timedate to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e89fb3cb", "r_snippet": "holidayNYSE()", "py_snippet": "    print(f\" [{i+1}] {formatted_chunk}\")\n\ndef get_nth_weekday(year, month, weekday, n):\n    # weekday: 0=Mon, 6=Sun\n    first_day = date(year, month, 1)\n    first_weekday = first_day.weekday()\n    offset = (weekday - first_weekday + 7) % 7\n    day = 1 + offset + (n - 1) * 7\n    return date(year, month, day)\n\ndef get_easter_date(year):\n    a = year % 19\n    b = year // 100\n    c = year % 100\n    d = b // 4\n    e = b % 4\n    f = (b + 8) // 25\n    g = (b - f + 1) // 3\n    h = (19 * a + b - d - g + 15) % 30\n    i = c // 4\n    k = c % 4\n    l = (32 + 2 * e + 2 * i - h - k) % 7\n    m = (a + 11 * h + 22 * l) // 451\n    month = (h + l - 7 * m + 114) // 31\n    day = ((h + l - 7 * m + 114) % 31) + 1\n    return date(year, month, day)\n\ndef holidayNYSE(year=None, type_val=\"\"):\n    if year is None:\n        year = getRmetricsOptions(\"currentYear\")\n    \n    years = [year] if isinstance(year, (int, float)) else year\n    holidays = []\n    \n    for y in years:\n        holidays.append(date(y, 1, 1))   # New Year\n        holidays.append(date(y, 7, 4))   # Independence Day\n        holidays.append(date(y, 12, 25)) # Christmas\n        holidays.append(get_nth_weekday(y, 11, 3, 4)) # Thanksgiving\n        holidays.append(get_nth_weekday(y, 9, 0, 1))  # Labor Day\n        holidays.append(get_nth_weekday(y, 10, 0, 2)) # Columbus Day\n        holidays.append(get_nth_weekday(y, 2, 0, 3))  # Presidents Day\n        if y >= 1998:\n            holidays.append(get_nth_weekday(y, 1, 0, 3)) # MLK\n        if y >= 2022:\n            holidays.append(date(y, 6, 19)) # Juneteenth\n        last_may = date(y, 5, 31)\n        offset = (last_may.weekday() - 0) % 7\n        holidays.append(last_may - timedelta(days=offset)) # Memorial Day\n        holidays.append(date(y, 11, 11)) # Veterans Day\n        good_friday = get_easter_date(y) - timedelta(days=2)\n        holidays.append(good_friday)\n\n    # R: ans[!(posix3$wday == 0 | posix3$wday == 6)]\n    biz_holidays = [h for h in holidays if h.weekday() != 5 and h.weekday() !=", "score": 0.9612, "script_id": "timeDate__rd_example__calendar-isBizday_Rd.R", "n_calls": 0}

## Edit Examples
(none)
