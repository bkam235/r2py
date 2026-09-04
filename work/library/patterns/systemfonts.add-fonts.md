---
id: systemfonts.add-fonts
package: systemfonts
confidence: tentative
seed: true
created: 2026-09-04
last_review: 2026-09-04
tie_count: 0
---

# systemfonts.add-fonts

## Guidance
Translate R `add_fonts` (FunctionCall from systemfonts) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "36a6f5c2", "r_snippet": "add_fonts(empty_font)", "py_snippet": "    def add_fonts(self, font_path):\n        # Mimics registering a font\n        pass\n\nsys_fonts.add_fonts(empty_font)\n\n# clear_local_fonts()", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
