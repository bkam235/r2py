---
id: rlang--is_installed
package: broom
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-22
tie_count: 0
---

# rlang--is_installed

## Guidance
Implement using a try-except block with __import__(package_name) to check if a module is available in the Python environment.

Use `importlib.util.find_spec(package_name) is not None` to check if a Python package is available.

Use 'importlib.util.find_spec(package_name) is not None' to check for the existence of a Python package.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
