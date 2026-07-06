---
id: bslib.popover
package: bslib
confidence: tentative
seed: true
created: 2026-07-05
last_review: 2026-07-05
tie_count: 0
---

# bslib.popover

## Guidance
Translate R `popover` (FunctionCall from bslib) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f2f7ef98", "r_snippet": "popover(\n  shiny::actionButton(\"btn\", \"A button\"),\n  \"Popover body content...\",\n  title = \"Popover title\"\n)", "py_snippet": "print(\n    ui.popover(\n        ui.input_action_button(\"btn\", \"A button\"),\n        \"Popover body content...\",\n        title=\"Popover title\"\n    )\n)\n\n            ui.popover(\n                ui.output_ui(\"card_title\", inline=True),\n                ui.input_text(\"card_title\", None, value=\"An editable title\"),\n                title=\"Provide a new title\"\n            )\n        ),\n        \"The card body...\",\n        class_=\"mt-5\"\n    )\n)", "score": 0.977, "script_id": "auto"}

## Edit Examples
(none)
