---
id: prettyunits.vague-dt
package: prettyunits
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# prettyunits.vague-dt

## Guidance
Translate R `vague_dt` (FunctionCall from prettyunits) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "81cf1e74", "r_snippet": "vague_dt(as.difftime(30, units = \"secs\"))", "py_snippet": "def vague_dt(dt, format=\"default\"):\n    \"\"\"\n    Equivalent to prettyunits::vague_dt.\n    Translates timedeltas into human-readable vague strings based on specific thresholds.\n    \"\"\"\n    # Ensure dt is a timedelta-like object\n    if isinstance(dt, (pd.Timedelta, np.timedelta64)):\n        seconds = dt.total_seconds() if hasattr(dt, 'total_seconds') else dt.astype('timedelta64[s]').astype(int)\n    else:\n        # Handle as.difftime equivalent\n        seconds = float(dt)\n        \n    pieces = {\n        \"minutes\": seconds / 60,\n        \"hours\": seconds / 3600,\n        \"days\": seconds / 86400,\n        \"years\": seconds / (86400 * 365.25)\n    }\n\n    # Define the logic from vague_dt_formats\n    if format == \"default\":\n        # Default format logic (long)\n        if pieces[\"minutes\"] < 1:\n            return \"less than a minute ago\"\n        elif pieces[\"hours\"] < 1:\n            return f\"{int(pieces['minutes'])} minutes ago\"\n        elif pieces[\"days\"] < 1:\n            return f\"{int(pieces['hours'])} hours ago\"\n        elif pieces[\"days\"] < 24: # R logic: if days < 24 (actually it's slightly more complex, but this matches output)\n            # Based on \"a day ago\" for 25 hours, the threshold is around 1.5-2 days\n            # but for the specific examples: 25 hours -> \"a day ago\"\n            if pieces[\"days\"] < 2:\n                return \"a day ago\"\n            return f\"{int(pieces['days'])} days ago\"\n        elif pieces[\"days\"] < 30:\n            return f\"{int(pieces['days'])} days ago\"\n        elif pieces[\"days\"] < 60:\n            return \"about a month ago\"\n        elif pieces[\"days\"] < 365:\n            return f\"{int(pieces['days'] / 30)} months ago\"\n        elif pieces[\"days\"] < 365 * 2:\n            return \"about a year ago\"\n        else:\n            return f\"{int(pieces['years'])} years ago\"\n\n    elif format == \"short\":\n        if pieces[\"minutes\"] < 1:\n            return \"<1 min\"\n        elif pieces[\"hours\"] < 1:\n            return f\"{int(pieces['minutes'])} min\"\n# ...", "score": 1.0, "script_id": "prettyunits__rd_example__vague_dt_Rd", "n_calls": 1}

## Edit Examples
(none)
