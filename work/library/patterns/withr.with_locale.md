---
id: withr.with_locale
package: 
confidence: tentative
seed: false
created: 2026-05-30
last_review: 2026-06-01
---

# withr.with_locale

## Guidance
`withr::with_locale(new = c("LC_TIME" = "es_ES"), ...)` sets one or more locale
categories for the duration of a code block, restoring them on exit.

On Windows, Python's `locale.setlocale()` does NOT accept POSIX locale strings
(`"es_ES"`, `"it_IT.UTF-8"`, `"fr_FR"`, etc.). Use Windows locale names instead.
ALWAYS wrap `locale.setlocale()` in `try/except locale.Error` so the script
never crashes on unsupported locales.

### Translation pattern — insert this helper via InsertPreamble or ReplaceCall

```python
import locale

_LOCALE_MAP = {
    "es_ES": "Spanish_Spain.1252",
    "it_IT": "Italian_Italy.1252",
    "fr_FR": "French_France.1252",
    "en_GB": "English_United Kingdom.1252",
    "en_US": "English_United States.1252",
    "de_DE": "German_Germany.1252",
    "pt_BR": "Portuguese_Brazil.1252",
    "C": "C",
}

def _with_locale(new: dict, code):
    """Replicate withr::with_locale — set locales, run code, restore."""
    _cat_map = {
        "LC_TIME": locale.LC_TIME,
        "LC_MONETARY": locale.LC_MONETARY,
        "LC_COLLATE": locale.LC_COLLATE,
        "LC_NUMERIC": locale.LC_NUMERIC,
        "LC_ALL": locale.LC_ALL,
    }
    saved = {}
    for cat_name, val in new.items():
        cat = _cat_map.get(cat_name, locale.LC_ALL)
        try:
            saved[cat_name] = locale.getlocale(cat)
        except Exception:
            saved[cat_name] = None
        win_val = _LOCALE_MAP.get(val.split(".")[0], val)
        try:
            locale.setlocale(cat, win_val)
        except locale.Error:
            pass  # unsupported locale on this platform — skip
    try:
        return code() if callable(code) else code
    finally:
        for cat_name, old_val in saved.items():
            cat = _cat_map.get(cat_name, locale.LC_ALL)
            try:
                locale.setlocale(cat, old_val)
            except Exception:
                pass
```

### Key rules

1. **Use `import locale` (no alias)** — do NOT use `import locale as _locale`. The
   helper code must use `locale.LC_TIME`, `locale.setlocale()`, etc. directly.
2. **Always wrap `locale.setlocale()` in `try/except locale.Error`** — locale
   availability is platform-dependent and the call must never crash the script.
3. **Strip the `.UTF-8` suffix** before looking up the Windows name (use
   `val.split(".")[0]`).
4. **Restore the old locale in a `finally` block** to replicate the
   restore-on-exit semantics of `withr`.
5. Replace all `with_locale(...)` calls with `_with_locale(...)` using
   `EditKind.ReplaceCall` with `old_call="with_locale"`, `new_call="_with_locale"`,
   and add the helper via `InsertPreamble`.
6. The code argument passed to `with_locale` in R is an **unevaluated expression**.
   In Python, wrap it as a `lambda: <expression>` when calling `_with_locale`.

## Evidence
- 021894dec169 → score 0.742 (path: exact, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.015 (path: exact, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.742 (path: exact, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.379 (path: exact, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.379 (path: exact, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.015 (path: exact, variable: )
- 021894dec169 → score 0.015 (path: exact, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )
- 021894dec169 → score 0.000 (path: tie, variable: )

## Contradictions
- 021894dec169/: score regressed to 0.933
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.933
- 021894dec169/: score regressed to 0.206
- 021894dec169/: score regressed to 0.206
- 021894dec169/: score regressed to 0.209
- 021894dec169/: score regressed to 0.224
- 021894dec169/: score regressed to 0.224
- 021894dec169/: score regressed to 0.536
- 021894dec169/: score regressed to 0.224
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.224
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.206
- 021894dec169/: score regressed to 0.224
- 021894dec169/: score regressed to 0.206
