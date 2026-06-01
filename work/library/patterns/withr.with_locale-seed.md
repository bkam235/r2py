---
id: withr.with_locale-seed
package: 
confidence: contradicted
seed: true
created: 2026-06-01
last_review: 2026-06-01
tie_count: 5
---

# withr.with_locale-seed

## Guidance
`withr::with_locale(new = c("LC_TIME" = "es_ES"), expr)` sets locale categories
temporarily, then restores them. Python's `locale.setlocale()` does NOT accept
POSIX locale strings ("es_ES", "it_IT.UTF-8", "fr_FR", etc.) on Windows — they
raise `locale.Error` and crash the script.

**Translation rule**: Copy the `_LOCALE_MAP` dict and `_with_locale` helper below
verbatim into your Python translation, then call `_with_locale(...)` instead of
using `locale.setlocale()` directly. Wrap the code body as a `lambda:`.

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

**Usage**:
- `with_locale(new = c("LC_TIME" = "es_ES"), plot(df$date, df$value))` →
  `_with_locale({"LC_TIME": "es_ES"}, lambda: plt.plot(df['date'], df['value']))`
- `result <- with_locale(c("LC_TIME" = "en_GB"), format(ISOdate(...), "%B"))` →
  `result = _with_locale({"LC_TIME": "en_GB"}, lambda: [datetime(2000, m, 1).strftime("%B") for m in range(1, 13)])`
- `with_locale(new = c("LC_MONETARY" = "it_IT"), Sys.localeconv())` →
  `result = _with_locale({"LC_MONETARY": "it_IT"}, lambda: locale.localeconv())`
- `with_locale(c(LC_COLLATE = "C"), sort(x))` →
  `result = _with_locale({"LC_COLLATE": "C"}, lambda: sorted(x))`

**Key rules**:
1. ALWAYS include the full `_LOCALE_MAP` dict in the same entity — NEVER call
   `locale.setlocale()` directly with POSIX strings like "es_ES" or "it_IT".
2. ALWAYS define `_with_locale` in the entity that first needs it; if already
   defined in a prior entity, just call it (do not redefine).
3. The code argument is always a `lambda: <expression>` — never an expression directly.
4. Add `import locale` to the imports list for every entity using locale.

## Evidence
(none)

## Contradictions
- 021894dec169/: score regressed to 0.000
- 021894dec169/: score regressed to 0.570
- 021894dec169/: score regressed to 0.933
- 021894dec169/: score regressed to 0.933
- 021894dec169/: score regressed to 0.933
