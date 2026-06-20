---
id: remove-invalid-imports
package: 
confidence: tentative
seed: false
created: 2026-06-06
last_review: 2026-06-06
tie_count: 0
---

# remove-invalid-imports

## Guidance
Remove import statements that reference non-existent functions or modules. In R→Python translation, when dataset loading is handled via inline definition (as with volcano), the corresponding import statement should be removed to prevent ImportError.

## Evidence
- dd2e0ea0b08b → score 0.057 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "import matplotlib.pyplot as plt\nimport numpy as np\nfrom datasets import load_dataset_volcano\nfrom scipy import io", "new_code": "import matplotlib.pyplot as plt\nimport numpy as np", "score_delta": 0.0567, "script_id": "dd2e0ea0b08b"}
