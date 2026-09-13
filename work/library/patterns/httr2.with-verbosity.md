---
id: httr2.with-verbosity
package: httr2
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# httr2.with-verbosity

## Guidance
Translate R `with_verbosity` (FunctionCall from httr2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f90d6ab0", "r_snippet": "with_verbosity(fun())", "py_snippet": "def local_verbosity(verbosity):\n    global _current_verbosity\n    _current_verbosity = verbosity\n\n@contextmanager\ndef verbosity_context(verbosity):\n    global _current_verbosity\n    old_verbosity = _current_verbosity\n    _current_verbosity = verbosity\n    try:\n        yield\n    finally:\n        _current_verbosity = old_verbosity\n\ndef with_verbosity(code, verbosity=1):\n    with verbosity_context(verbosity):\n        # In R, with_verbosity(fun()) evaluates fun() within the context\n        return code\n\ndef request(url):\n    # Simplified request object\n    return {\"url\": url, \"method\": \"GET\", \"head", "score": 0.9089, "script_id": "auto"}

## Edit Examples
(none)
