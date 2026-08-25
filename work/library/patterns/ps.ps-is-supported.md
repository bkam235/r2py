---
id: ps.ps-is-supported
package: ps
confidence: tentative
seed: true
created: 2026-08-25
last_review: 2026-08-25
tie_count: 0
---

# ps.ps-is-supported

## Guidance
Translate R `ps_is_supported` (ExternalSymbol from ps) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c3f80b69", "r_snippet": "if (ps::ps_is_supported() && ! ps:::is_cran_check() && ps::ps_os_type()[\"POSIX\"]) (if (getRversion() >= \"3.4\") withAutoprint else force)({ # examplesIf", "py_snippet": "try:\n    # p1 <- processx::process$new(\"sleep\", \"100\")", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
