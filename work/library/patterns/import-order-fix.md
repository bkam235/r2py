---
id: import-order-fix
package: 
confidence: confirmed
seed: false
created: 2026-06-07
last_review: 2026-06-14
tie_count: 0
---

# import-order-fix

## Guidance
Move all imports to the top of the script before any code uses them. In Python, `import` statements must execute before the imported names can be used, or a NameError will result.

## Evidence
- dd2e0ea0b08b → score 0.067 (path: exact, variable: )
- d42c7e223bcd → score 0.460 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "699c0442", "r_snippet": "suppressPackageStartupMessages(library(shape))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "d42c7e223bcd"}
- {"r_hash": "258fd16a", "r_snippet": "all_equal(mtcars, mtcars2)", "py_snippet": "# In R: all_equal(mtcars, mtcars2)\nprint(f\"[1] {all_equal_func(mtcars, mtcars2)}\")", "score": 1.0, "script_id": "9c532ab9a0a0"}
- {"r_hash": "edc0e14b", "r_snippet": "all.equal(\n  mtcars,\n  mtcars2[rownames(mtcars), names(mtcars)]\n)", "py_snippet": "# In R: all.equal(mtcars, mtcars2[rownames(mtcars), names(mtcars)])\n# We use all_equal_func with ignore_row_order=False to simulate all.equal \n# after the user has explicitly re-ordered the data.\ntry:\n    # Reorder mtcars2 to match mtcars indices and columns\n    mtcars2_reordered = mtcars2.loc[mtcars.index, mtcars.columns]\n    print(f\"[1] {all_equal_func(mtcars, mtcars2_reordered, ignore_row_order=False, ignore_col_order=False)}\")\nexcept Exception:\n    print(\"[1] FALSE\")", "score": 1.0, "script_id": "9c532ab9a0a0"}

## Edit Examples
- {"failure_class": "stdout", "old_code": "# Translated from <R script> by r2py v0.2.0\n# Model: claude-haiku-4-5  ScriptMap entities: 5\n\n# Load volcano dataset (87x61 matrix)\n# Load volcano dataset from R\nfrom sklearn.datasets import load_sample_image\ntry:", "new_code": "# Translated from <R script> by r2py v0.2.0\n# Model: claude-haiku-4-5  ScriptMap entities: 5\n\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom matplotlib.colors import ListedColormap, to_rgb\n\n# Load volcano dataset (87x61 matrix)\n# Load volcano dataset from R\nfrom sklearn.datasets import load", "score_delta": 0.4605, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "# Translated from <R script> by r2py v0.2.0\n# Model: claude-haiku-4-5  ScriptMap entities: 5\n\n# Load the volcano dataset (standard R built-in dataset)\n# 87x61 matrix with elevation data\nvolcano = np.array([", "new_code": "# Translated from <R script> by r2py v0.2.0\n# Model: claude-haiku-4-5  ScriptMap entities: 5\n\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport warnings\nfrom matplotlib.colors import ListedColormap\nfrom scipy.io import loadmat\nfrom statsmodels.datasets import co2\n\n# Load the volcano dataset ", "score_delta": 0.0667, "script_id": "dd2e0ea0b08b"}
