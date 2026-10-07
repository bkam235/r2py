---
id: base.sort
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.sort

## Guidance
Translate R `sort` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c3667b23", "r_snippet": "simulated <- data.frame(obs = factor(rep(letters[1:2], each = 100)),\n                        perfect = sort(runif(200), decreasing = TRUE),\n                        random = runif(200))", "py_snippet": "simulated = pd.DataFrame({\n    'obs': pd.Categorical(np.repeat(list(string.ascii_lowercase[:2]), 100), categories=list(string.ascii_lowercase[:2])),\n    'perfect': np.sort(np.random.uniform(0, 1, 200))[::-1],\n    'random': np.random.uniform(0, 1, 200)", "score": 1.0, "script_id": "caret__rd_example__lift_Rd.R", "n_calls": 5}

## Edit Examples
(none)
