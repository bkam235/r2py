---
id: base.dataframe_to_pandas
package: base
confidence: contradicted
seed: true
created: 2026-05-28
last_review: 2026-06-04
tie_count: 10
---

# base.dataframe_to_pandas

## Guidance
Translate `data.frame(col1=..., col2=...)` to `pd.DataFrame({"col1": ..., "col2": ...})`.
Import pandas as `import pandas as pd`. Column names map directly. R's recycling of
shorter vectors must be handled explicitly in Python — pad or repeat shorter lists to
match the longest column length.

## Evidence
(none)

## Contradictions
- 021894dec169/: score regressed to 0.848
- 021894dec169/: score regressed to 0.238
- 021894dec169/: score regressed to 0.238
- 021894dec169/: score regressed to 0.242
- 021894dec169/: score regressed to 0.238
