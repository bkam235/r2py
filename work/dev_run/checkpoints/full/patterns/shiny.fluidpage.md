---
id: shiny.fluidpage
package: shiny
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# shiny.fluidpage

## Guidance
Translate R `fluidPage` (FunctionCall from shiny) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cacb80e4", "r_snippet": "ui <- fluidPage(\n  actionButton(\"rmv\", \"Remove UI\"),\n  textInput(\"txt\", \"This is no longer useful\")\n)", "py_snippet": "ui_2 = ui.page_fluid(\n    ui.input_action_button(\"rmv\", \"Remove UI\"),\n    ui.input_text(\"txt\", \"This is no longer useful\")\n)", "score": 1.0, "script_id": "shiny__rd_example__insertUI_Rd", "n_calls": 0}

## Edit Examples
(none)
