---
id: utils.str
package: utils
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# utils.str

## Guidance
Translate R `str` (FunctionCall from utils) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "3a024097", "r_snippet": "str(\n  sparse_character(c(\"A\", \"C\", \"E\"), c(2, 5, 10), 1000000000)\n)", "py_snippet": "def str_summary(obj):\n    if isinstance(obj, SparseCharacterVector):\n        # R output: chr [1:1000000000] \"\" \"A\" \"\" \"\" \"C\" \"\" \"\" \"\" \"\" \"E\" \"\" \"\" \"\" \"\" \"\" \"\" \"\" ...\n        # It shows the first few elements\n        preview = []\n        for i in range(min(obj.length, 20)):\n            val = obj[i]\n            preview.append(f'\"{val}\"' if val != \"\" else '\"\"')\n        \n        preview_str = \" \".join(preview)\n        if obj.length > 20:\n            preview_str += \" ...\"\n            \n        return f\"chr [1:{obj.length}] {preview_str}\"\n    return str(obj)\n\n# Execution\n# sparse_character(character(", "score": 1.0, "script_id": "auto"}
- {"r_hash": "01a8948c", "r_snippet": "data(benchmark64.data)", "py_snippet": "if 'benchmark64.data' in globals():\n    # If the shim loaded it as a list of lists/dicts, convert to DataFrame\n    # R's benchmark64.data usually has row names and col names.\n    # Based on R output: rows are tasks, cols are contexts.\n    raw_data = globals()['benchmark64.data']\n    if isinstance(raw_data, dict):\n        # Handle case where it might be a dict representing a dataframe\n        benchmark64_data = pd.DataFrame(raw_data)\n    else:\n        # Handle list/array representation\n        benchmark64_data = pd.DataFrame(raw_data)\nelse:\n    # Fallback if shim fails (though it shouldn't)\n   ", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)
