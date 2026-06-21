---
id: with-locale
package: 
confidence: tentative
seed: true
created: 2026-06-05
last_review: 2026-06-21
tie_count: 18
---

# with-locale

## Guidance
Translate R `with_locale` (FunctionCall from base R) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
- 021894dec169 → score 0.083 (path: exact, variable: )
- 021894dec169 → score 0.083 (path: exact, variable: )
- 021894dec169 → score 0.083 (path: exact, variable: )
- 021894dec169 → score 0.411 (path: exact, variable: )
- 021894dec169 → score 0.083 (path: exact, variable: )
- 021894dec169 → score 0.083 (path: exact, variable: )
- 021894dec169 → score 0.083 (path: exact, variable: )

## Contradictions
- 021894dec169/: score regressed to 0.864
- 021894dec169/: score regressed to 0.864
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.738
- 021894dec169/: score regressed to 0.268
- 021894dec169/: score regressed to 0.461

## Translation Examples
- {"r_hash": "c301d570", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"es_ES\"), code = plot(df$date, df$value))", "py_snippet": "# Save original locale\n_original_locale = locale.getlocale(locale.LC_TIME)\n\ntry:\n    # Attempt to set Spanish locale for time\n    try:\n        locale.setlocale(locale.LC_TIME, \"es_ES\")\n    except locale.Error:\n        # Silently skip on Windows or unsupported locales\n        pass\n    \n    # Execute the plotting code\n    plt.plot(df['date'], df['value'])\n    plt.show()\n    \nfinally:\n    # Restore original locale\n    try:\n        if _original_locale[0]:\n            locale.setlocale(locale.LC_TIME, _original_locale)\n        else:\n            locale.setlocale(locale.LC_TIME, \"C\")\n    except locale", "score": 1.0, "script_id": "human-verified"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "with_locale(new={\"LC_TIME\": \"es_ES\"}, func=lambda: # plot(df[\"date\"], df[\"value\"])  # Requires matplotlib)", "new_code": "with_locale(new={\"LC_TIME\": \"es_ES\"}, func=lambda: None)", "score_delta": 0.4106, "script_id": "021894dec169"}
- {"failure_class": "stdout", "old_code": "result = with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [datetime.fromisoformat(d).strftime(\"%B\") for d in ISOdate(2000, list(range(1, 13)), 1)]\n)", "new_code": "print(with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [datetime.fromisoformat(d).strftime(\"%B\") for d in ISOdate(2000, list(range(1, 13)), 1)]\n))", "score_delta": 0.0833, "script_id": "021894dec169"}
- {"failure_class": "stdout", "old_code": "with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [date(2000, month, 1).strftime(\"%B\") for month in range(1, 13)]\n)", "new_code": "print(with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [date(2000, month, 1).strftime(\"%B\") for month in range(1, 13)]\n))", "score_delta": 0.0833, "script_id": "021894dec169"}
- {"failure_class": "stdout", "old_code": "# ISOdate(2000, 1:12, 1) produces dates for Jan 1 through Dec 1, 2000\n# format(..., \"%B\") produces month names\n# with_locale temporarily sets LC_TIME to \"en_GB\" for the format call\n\nresult = with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [\n        datetime.datetime(2000, month, 1).strft", "new_code": "# ISOdate(2000, 1:12, 1) produces dates for Jan 1 through Dec 1, 2000\n# format(..., \"%B\") produces month names\n# with_locale temporarily sets LC_TIME to \"en_GB\" for the format call\n\nwith_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: print([datetime.datetime(2000, month, 1).strftime(\"%B\") fo", "score_delta": 0.0833, "script_id": "021894dec169"}
- {"failure_class": "stdout", "old_code": "# ISOdate(2000, 1:12, 1) produces dates for Jan 1 through Dec 1, 2000\n# format(..., \"%B\") produces month names\n# with_locale temporarily sets LC_TIME to \"en_GB\" for the format call\n\nresult = with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [\n        datetime.datetime(2000, month, 1).strft", "new_code": "# ISOdate(2000, 1:12, 1) produces dates for Jan 1 through Dec 1, 2000\n# format(..., \"%B\") produces month names\n# with_locale temporarily sets LC_TIME to \"en_GB\" for the format call\n\nprint(with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [\n        datetime.datetime(2000, month, 1).strftime", "score_delta": 0.0833, "script_id": "021894dec169"}
- {"failure_class": "graphics", "old_code": "result = with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [datetime.fromisoformat(d).strftime(\"%B\") for d in ISOdate(2000, list(range(1, 13)), 1)]\n)", "new_code": "with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: print([datetime.fromisoformat(d).strftime(\"%B\") for d in ISOdate(2000, list(range(1, 13)), 1)])\n)", "score_delta": 0.0833, "script_id": "021894dec169"}
- {"failure_class": "graphics", "old_code": "result = with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [datetime.fromisoformat(d).strftime(\"%B\") for d in ISOdate(2000, list(range(1, 13)), 1)]\n)", "new_code": "result = with_locale(\n    new={\"LC_TIME\": \"en_GB\"},\n    func=lambda: [datetime.fromisoformat(d).strftime(\"%B\") for d in ISOdate(2000, list(range(1, 13)), 1)]\n)\nprint(result)", "score_delta": 0.0833, "script_id": "021894dec169"}
