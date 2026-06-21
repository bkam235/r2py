---
id: package-internal-access
package: googlesheets4
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# package-internal-access

## Guidance
R's triple-colon operator `package:::function` accesses internal/unexported objects; in Python, these should be translated as attributes of the module (e.g., `module.function`) assuming the Python wrapper exposes them.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
