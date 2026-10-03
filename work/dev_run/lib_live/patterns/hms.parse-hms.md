---
id: hms.parse-hms
package: hms
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# hms.parse-hms

## Guidance
Translate R `parse_hms` (FunctionCall from hms) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9ccfaee9", "r_snippet": "parse_hms(\"12:34:56\")", "py_snippet": "def hms(seconds=None, minutes=None, hours=None, days=None):\n    \"\"\"\n    Equivalent to the hms function which calculates total seconds.\n    \"\"\"\n    total_secs = 0.0\n    if days is not None:\n        total_secs += days * 86400\n    if hours is not None:\n        total_secs += hours * 3600\n    if minutes is not None:\n        total_secs += minutes * 60\n    if seconds is not None:\n        total_secs += seconds\n    \n    # R's hms returns a specialized duration object. In Python, \n    # we represent this as a timedelta or the total seconds.\n    return timedelta(seconds=total_secs)\n\ndef parse_time(x, format_str):\n    \"\"\"\n    Helper to parse time strings based on a format.\n    \"\"\"\n    if x is None or x == \"\":\n        return hms()\n    \n    # Mimic R's strptime logic by adding a base date\n    full_str = f\"1970-01-01 {x}\"\n    full_format = f\"%Y-%m-%d {format_str}\"\n    \n    try:\n        dt = datetime.strptime(full_str, full_format)\n        # R's parse_time uses mday to handle overflows or specific offsets\n        # For standard time strings, we extract hours, minutes, seconds\n        return hms(\n            hours=dt.hour, \n            minutes=dt.minute, \n            seconds=dt.second + (dt.microsecond / 1_000_000)\n        )\n    except ValueError:\n        return None\n\ndef parse_hms(x):\n    \"\"\"\n    Parse string as hours:minutes:seconds.\n    \"\"\"\n    # %OS in R allows for fractional seconds. \n    # Python's %S is seconds, we handle the fraction via datetime.\n    # We adjust the format to be compatible with strptime.\n    fmt = \"%H:%M:%S\"\n    if \".\" in x:\n        # If milliseconds are present, %S in Python handles them if using %f\n        # but strptime is strict. We'll manually handle common R %OS cases.\n        # For simplicity in this translation, we adapt the format.\n        fmt = \"%H:%M:%S.%f\"\n    \n    return parse_time(x, fmt)\n\nprint(parse_hms(\"12:34:56\"))", "score": 1.0, "script_id": "hms__rd_example__parse_hms_Rd", "n_calls": 0}

## Edit Examples
(none)
