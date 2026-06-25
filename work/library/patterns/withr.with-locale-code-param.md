---
id: withr.with-locale-code-param
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-25
tie_count: 1
---

# withr.with-locale-code-param

## Guidance
In R's withr::with_locale(), the 'code' parameter accepts an expression to execute within the modified locale context. In Python, the context manager signature should accept an optional code callable parameter that is executed within the contextmanager's try block, allowing the function to be called with code= argument as in R.

## Evidence
- 021894dec169 → score 0.059 (path: exact, variable: )
- 021894dec169 → score 0.189 (path: exact, variable: )
- 021894dec169 → score 0.256 (path: exact, variable: )

## Contradictions
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.486
- 021894dec169/: score regressed to 0.551
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.461
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.385
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.373
- 021894dec169/: score regressed to 0.385
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.504
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.532
- 021894dec169/: score regressed to 0.532
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.380
- 021894dec169/: score regressed to 0.385
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000

## Translation Examples
- {"r_hash": "e94e70f7", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"en_GB\"), format(ISOdate(2000, 1:12, 1), \"%B\"))", "py_snippet": "with with_locale(new={\"LC_TIME\": \"en_GB\"}):\n    print(\" \".join([dt.datetime(2000, month, 1).strftime(\"%B\") for month in range(1, 13)]))", "score": 1.0, "script_id": "021894dec169"}
- {"r_hash": "35d704fc", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"es_ES\"), format(ISOdate(2000, 1:12, 1), \"%B\"))", "py_snippet": "# The with_locale context manager is already defined.\n# Call it with the R code parameters and handle the result.\n\ndef format_iso_dates_in_locale(locale_dict):\n    \"\"\"\n    Format ISO dates (2000-01-01 to 2000-12-01) as month names in Spanish locale.\n    \"\"\"\n    months = []\n    with with_locale(new=locale_dict):\n        for month in range(1, 13):\n            # Create date for year 2000, month 1-12, day 1\n            date_obj = datetime(2000, month, 1)\n            # Format as month name (%B)\n            month_name = date_obj.strftime(\"%B\")\n            months.append(month_name)\n    return months\n", "score": 1.0, "script_id": "021894dec169"}
- {"r_hash": "1f66ba44", "r_snippet": "with_locale(c(LC_COLLATE = \"fr_FR\"), sort(x))", "py_snippet": "with with_locale({\"LC_COLLATE\": \"fr_FR\"}):\n    print(sorted(x))", "score": 1.0, "script_id": "021894dec169"}

## Edit Examples
- {"failure_class": "data", "old_code": "@contextlib.contextmanager\ndef with_locale(new):\n    \"\"\"\n    Context manager for temporarily modified locale settings.\n    \n    Args:\n        new: dict mapping locale category names (e.g., \"LC_TIME\") to locale strings\n    \n    Yields:\n        None (use as 'with with_locale(new): ...')\n    \"\"\"\n    # ", "new_code": "def with_locale(new, code=None):\n    \"\"\"\n    Temporarily modify locale settings and execute code.\n    \n    Args:\n        new: dict mapping locale category names (e.g., \"LC_TIME\") to locale strings\n        code: callable to execute within the modified locale context, or None for context manager use\n ", "score_delta": 0.1889, "script_id": "021894dec169"}
- {"failure_class": "graphics", "old_code": "@contextlib.contextmanager\ndef with_locale(new: Dict[str, str]):\n    \"\"\"\n    Context manager to temporarily change locale settings.\n    \n    Args:\n        new: Dictionary of locale category -> locale name mappings\n             e.g., {\"LC_TIME\": \"es_ES\"}\n    \"\"\"\n    # Store old locale values\n    old_", "new_code": "@contextlib.contextmanager\ndef with_locale(new: Dict[str, str], code: Optional[Callable] = None):\n    \"\"\"\n    Context manager to temporarily change locale settings.\n    \n    Args:\n        new: Dictionary of locale category -> locale name mappings\n             e.g., {\"LC_TIME\": \"es_ES\"}\n        code:", "score_delta": 0.2562, "script_id": "021894dec169"}
- {"failure_class": "graphics", "old_code": "@contextlib.contextmanager\ndef with_locale(new):\n    \"\"\"\n    Context manager for temporarily modified locale settings.\n    \n    Args:\n        new: dict mapping locale category names (e.g., \"LC_TIME\") to locale strings\n    \n    Yields:\n        None (use as 'with with_locale(new): ...')\n    \"\"\"\n    # ", "new_code": "@contextlib.contextmanager\ndef with_locale(new, code=None):\n    \"\"\"\n    Context manager for temporarily modified locale settings.\n    \n    Args:\n        new: dict mapping locale category names (e.g., \"LC_TIME\") to locale strings\n        code: optional code block to execute within the locale context\n", "score_delta": 0.0589, "script_id": "021894dec169"}
