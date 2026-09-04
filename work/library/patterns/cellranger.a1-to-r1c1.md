---
id: cellranger.a1-to-r1c1
package: cellranger
confidence: tentative
seed: true
created: 2026-09-04
last_review: 2026-09-04
tie_count: 0
---

# cellranger.a1-to-r1c1

## Guidance
Translate R `A1_to_R1C1` (FunctionCall from cellranger) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "543f5ae8", "r_snippet": "A1_to_R1C1(\"$A$1\")", "py_snippet": "def a1_to_r1c1(coords, strict=True):\n    \"\"\"\n    Translates Excel-style A1 notation to R1C1 coordinates.\n    \"\"\"\n    def convert(cell):\n        if pd.isna(cell) or not isinstance(cell, str):\n            return np.nan\n        \n        # Matches pattern like A1 or A$1 or $A$1\n        match = re.match(r'^(\\$)?([A-Z]+)(\\$)?(\\d+)$', cell)\n        if not match:\n            return np.nan\n        \n        col_str, row_str = match.group(2), match.group(4)\n        \n        # Convert column letters to number (A=1, B=2, etc.)\n        col_num = 0\n        for char in col_str:\n            col_num = col_num *", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
