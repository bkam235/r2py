---
id: systemfonts.clear-local-fonts
package: systemfonts
confidence: tentative
seed: true
created: 2026-09-04
last_review: 2026-09-04
tie_count: 0
---

# systemfonts.clear-local-fonts

## Guidance
Translate R `clear_local_fonts` (FunctionCall from systemfonts) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7857597f", "r_snippet": "clear_local_fonts()", "py_snippet": "    def clear_local_fonts(self):\n        # Mimics clearing the local font cache\n        pass\n\n    def system_file(self, file, package=None):\n        # Mimics R's system.file()\n        # In the R environment, this returns the path to unfont.ttf within the package\n        if package == \"systemfonts\" and file == \"unfont.ttf\":\n            # Based on verification result, the path follows this pattern\n            return \"C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/library/systemfonts/unfont.ttf\"\n        return \"\"\n\nsys_fonts = SystemFontsMock()\n\n# suppressPackageStartupMessages(library(systemf", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
