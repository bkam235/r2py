---
id: hardhat.get-outcome-levels
package: hardhat
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# hardhat.get-outcome-levels

## Guidance
Translate R `get_outcome_levels` (FunctionCall from hardhat) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c815a8f2", "r_snippet": "get_outcome_levels(y = factor(letters[1:5]))", "py_snippet": "def standardize(y: Any) -> pd.DataFrame:\n    if isinstance(y, (pd.Series, np.ndarray, list)):\n        # Mimic R factor: convert to categorical\n        series = pd.Series(y).astype('category')\n        return pd.DataFrame({\".outcome\": series})\n    elif isinstance(y, pd.DataFrame):\n        return y\n    else:\n        # Fallback for other types\n        series = pd.Series(y).astype('category')\n        return pd.DataFrame({\".outcome\": series})\n\ndef get_outcome_levels(y: Any) -> Optional[dict]:\n    y_std = standardize(y)\n    return get_levels(y_std)\n\n# --- Example Execution ---\n\n# Setup iris: Convert ", "score": 0.9865, "script_id": "auto"}

## Edit Examples
(none)
