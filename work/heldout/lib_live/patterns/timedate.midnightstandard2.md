---
id: timedate.midnightstandard2
package: timeDate
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# timedate.midnightstandard2

## Guidance
Translate R `midnightStandard2` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2707750f", "r_snippet": "(ms2 <- midnightStandard2(ch))", "py_snippet": "def midnightStandard2(charvec, format_val=None):\n    if format_val is None:\n        format_val = whichFormat(charvec)\n    \n    # Handle the \"24:00\" case which strptime cannot parse\n    # R's midnightStandard2 converts 24:00 to 00:00 of the next day\n    if \"24:00\" in charvec:\n        date_part = charvec.split(\" \")[0]\n        dt = datetime.strptime(date_part, \"%Y-%m-%d\") + timedelta(days=1)\n        return pd.Timestamp(dt, tz='GMT')\n    \n    return pd.to_datetime(charvec, format=format_val, utc=True)\n\nms2 = midnightStandard2(ch)\n# R prints POSIXct as \"2008-01-01 GMT\" for this case\nprint(f'[1] \"{ms2.strftime(\"%Y-%m-%d GMT\")}\"')\n\n# R's class(ms2) returns c(\"POSIXct\", \"POSIXt\")", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-midnightStandard_Rd", "n_calls": 0}

## Edit Examples
(none)
