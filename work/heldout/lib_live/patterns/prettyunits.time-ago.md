---
id: prettyunits.time-ago
package: prettyunits
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# prettyunits.time-ago

## Guidance
Translate R `time_ago` (FunctionCall from prettyunits) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "67e90aea", "r_snippet": "time_ago(now)", "py_snippet": "VAGUE_DT_FORMATS = {\n    \"default\": [\n        (lambda p: p['seconds'] < 1, lambda p: \"moments ago\"),\n        (lambda p: p['minutes'] < 1, lambda p: \"less than a minute ago\"),\n        (lambda p: p['minutes'] < 60, lambda p: f\"{int(p['minutes'])} minute{'s' if p['minutes'] != 1 else ''} ago\"),\n        (lambda p: p['hours'] < 24, lambda p: f\"{int(p['hours'])} hour{'s' if p['hours'] != 1 else ''} ago\"),\n        (lambda p: p['days'] < 2, lambda p: \"a day ago\"),\n        (lambda p: p['days'] < 30, lambda p: f\"{int(p['days'])} days ago\"),\n        (lambda p: p['days'] < 365, lambda p: \"about a month ago\"),\n        (lambda p: p['years'] < 2, lambda p: \"about a year ago\"),\n        (lambda p: True, lambda p: f\"{int(p['years'])} years ago\"),\n    ],\n    \"short\": [\n        (lambda p: p['minutes'] < 1, lambda p: \"<1 min\"),\n        (lambda p: p['minutes'] < 60, lambda p: f\"{int(p['minutes'])} min\"),\n        (lambda p: p['hours'] < 24, lambda p: f\"{int(p['hours'])} hours\"),\n        (lambda p: p['days'] < 30, lambda p: f\"{int(p['days'])} day\"),\n        (lambda p: p['days'] < 365, lambda p: \"1 mon\"),\n        (lambda p: p['years'] < 2, lambda p: \"1 year\"),\n        (lambda p: True, lambda p: f\"{int(p['years'])} years\"),\n    ],\n    \"terse\": [\n        (lambda p: p['minutes'] < 1, lambda p: f\"{int(p['seconds'])}s\"),\n        (lambda p: p['minutes'] < 60, lambda p: f\"{int(p['minutes'])}m\"),\n        (lambda p: p['hours'] < 24, lambda p: f\" {int(p['hours'])}h\"),\n        (lambda p: p['days'] < 30, lambda p: f\" {int(p['days'])}d\"),\n        (lambda p: p['days'] < 365, lambda p: f\" 1M\"),\n        (lambda p: p['years'] < 2, lambda p: f\" 1y\"),\n        (lambda p: True, lambda p: f\"{int(p['years'])}y\"),\n    ]\n}\n\ndef vague_dt(dt, format=\"default\"):\n    seconds = float(dt)\n    pieces = {\n        \"seconds\": seconds,\n        \"minutes\": seconds / 60,\n        \"hours\": seconds / 3600,\n        \"days\": seconds / 86400,\n        \"years\": seconds / (86400 * 365.25)\n    }\n    \n# ...", "score": 1.0, "script_id": "prettyunits__rd_example__time_ago_Rd", "n_calls": 0}

## Edit Examples
(none)
