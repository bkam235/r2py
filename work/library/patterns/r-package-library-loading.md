---
id: r-package-library-loading
package: broom
confidence: tentative
seed: false
created: 2026-06-24
last_review: 2026-06-24
tie_count: 0
---

# r-package-library-loading

## Guidance
Translate `library(package)` and `suppressPackageStartupMessages(library(...))` to `pass` or a print statement, since Python packages are imported differently. For data packages, use a data shim to load serialized data from JSON.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
