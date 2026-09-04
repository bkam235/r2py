---
id: pillar.tbl-format-header
package: pillar
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# pillar.tbl-format-header

## Guidance
Translate R `tbl_format_header` (FunctionCall from pillar) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ce74f360", "r_snippet": "tbl_format_header(palmerpenguins::penguins, setup)", "py_snippet": "def tbl_format_header(x, setup=None):\n    \"\"\"\n    Mimics pillar::tbl_format_header by printing the tibble-style \n    header summary: '# A tibble: rows × cols'\n    \"\"\"\n    if setup is None:\n        # If only setup is passed (as in the second R call), \n        # we extract the info from the setup object.\n        if isinstance(x, dict) and 'shape' in x:\n            setup = x\n        else:\n            # Handle cases where the first arg is meant to be the setup\n            setup = x\n    else:\n        # If both df and setup are passed, use the setup\n        pass\n        \n    # Ensure we have the sha", "score": 1.0, "script_id": "auto"}
- {"r_hash": "b16fd2ac", "r_snippet": "format_glimpse(1:3)", "py_snippet": "def format_glimpse(x, inner=False):\n    # Handle character/string types\n    if isinstance(x, (str, np.ndarray)) and (isinstance(x, str) or (x.dtype.kind in 'SU')):\n        # R's encodeString(quote=\"\\\"\") wraps strings in double quotes\n        if isinstance(x, str):\n            return f'\"{x}\"'\n        return np.array([f'\"{val}\"' for val in x])\n\n    # Handle Factors (Categorical in pandas)\n    if isinstance(x, pd.Categorical):\n        # If any level contains a comma, quote them\n        if any(',' in str(level) for level in x.categories):\n            return np.array([f'\"{val}\"' for val in x])\n    ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
