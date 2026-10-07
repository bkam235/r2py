---
id: base.rep-len
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.rep-len

## Guidance
Translate R `rep-len` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "73c67837", "r_snippet": "val2 <- c(\"\\033[45m\", rep_len(val, length(x)))", "py_snippet": "x0 = x1 = x2 = x3 = [\"\\033[42mABC\", \"\\033[34mDEF\"]\nx1 = substr_ctl_replace(x1, 2, 2, \"_\")\nx2 = substr_ctl_replace(x2, 2, 2, \"\\033[m_\")\nx3 = substr_ctl_replace(x3, 2, 2, \"\\033[45m_\")\nwriteLines(x0 + [end] + x1 + [end] + x2 + [end] + x3 + [end])\n\nx0 = x1 = x2 = x3 = [\"\\033[42mABC\", \"\\033[34mDEF\"]\nx0 = substr_ctl_replace(x0, 2, 2, \"_\", carry=True)", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd.R", "n_calls": 2}

## Edit Examples
(none)
