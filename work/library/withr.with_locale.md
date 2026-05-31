---
id: withr.with_locale
package: withr
confidence: confirmed
created: 2026-05-30
last_review: 2026-05-30
---

## Guidance

`withr::with_locale(new = c("LC_TIME" = "es_ES"), ...)` sets one or more locale
categories for the duration of a code block, restoring them on exit.

On Windows, Python's `locale.setlocale()` does NOT accept POSIX locale strings
(`"es_ES"`, `"it_IT.UTF-8"`, `"fr_FR"`, etc.). Use Windows locale names instead
(`"Spanish_Spain.1252"`, `"Italian_Italy.1252"`, `"French_France.1252"`, etc.).

### Translation pattern

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
}

def _with_locale(new: dict, code):
    """Replicate withr::with_locale — set locales, run code, restore."""
    saved = {}
    category_map = {
        "LC_TIME": locale.LC_TIME,
        "LC_MONETARY": locale.LC_MONETARY,
        "LC_COLLATE": locale.LC_COLLATE,
        "LC_NUMERIC": locale.LC_NUMERIC,
        "LC_ALL": locale.LC_ALL,
    }
    for cat_name, val in new.items():
        cat = category_map.get(cat_name, locale.LC_ALL)
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
        return code()
    finally:
        for cat_name, old_val in saved.items():
            cat = category_map.get(cat_name, locale.LC_ALL)
            try:
                locale.setlocale(cat, old_val)
            except Exception:
                pass

# Usage:
result = _with_locale({"LC_TIME": "es_ES"}, lambda: some_expression)
```

### Key rules

1. **Always wrap `locale.setlocale()` in `try/except locale.Error`** — locale
   availability is platform-dependent and the call must never crash the script.
2. **Strip the `.UTF-8` suffix** before looking up the Windows name (use
   `val.split(".")[0]`).
3. **Restore the old locale in a `finally` block** to replicate the
   restore-on-exit semantics of `withr`.
4. **Use `EditKind.ReplaceCall`** with `old_call = "with_locale"` and
   `new_call = "_with_locale"`, or `InsertPreamble` to add the helper function.

## Evidence

- script: withr__rd_example__with_locale_Rd.R — Windows locale.Error crash
  was root cause of score 0.212; locale strings `it_IT`, `es_ES`, `fr_FR`,
  `en_GB`, `en_US` all need Windows mapping.
