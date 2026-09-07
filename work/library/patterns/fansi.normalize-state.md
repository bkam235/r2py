---
id: fansi.normalize-state
package: fansi
confidence: tentative
seed: true
created: 2026-09-07
last_review: 2026-09-07
tie_count: 0
---

# fansi.normalize-state

## Guidance
Translate R `normalize_state` (FunctionCall from fansi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "06524759", "r_snippet": "normalize_state(\"hello\\033[42;33m world\")", "py_snippet": "def normalize_state(text, carry=\"\"):\n    \"\"\"\n    Equivalent to fansi::normalize_state.\n    Normalizes ANSI escape sequences by keeping only the final state \n    and removing redundant or unused closing codes.\n    \"\"\"\n    # combine carry and text to evaluate current state\n    full_text = carry + text\n    \n    # Match ANSI SGR (Select Graphic Rendition) sequences: \\033[...m\n    # We need to track the state changes.\n    \n    # Rule 1: Multiple consecutive SGR sequences: only the last one prevails if they are additive.\n    # R's fansi handles state by effectively flattening sequences of codes.\n   ", "score": 0.859, "script_id": "auto"}

## Edit Examples
(none)
