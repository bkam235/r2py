---
id: shiny.shinyapp
package: shiny
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# shiny.shinyapp

## Guidance
Translate R `shinyApp` (FunctionCall from shiny) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "eba54108", "r_snippet": "shinyApp(\n  ui = basicPage(\n    actionButton(\"show\", \"Show modal dialog\")\n  ),\n  server = function(input, output) {\n    observeEvent(input$show, {\n      showModal(modalDialog(\n        title = \"Important message\",\n        \"This is an important message!\"\n      ))\n    })\n  }\n)", "py_snippet": "def server1(input, output, session):\n    @reactive.effect\n    def _():\n        if input.show():\n            ui.show_modal(\n                ui.modal_dialog(\n                    \"This is an important message!\",\n                    title=\"Important message\"\n                )\n            )\n\napp1 = App(\n    ui=ui.page_bootstrap(\n        ui.input_action_button(\"show\", \"Show modal dialog\")\n    ),\n    server=server1\n)\n\n# --- App 2 ---", "score": 1.0, "script_id": "shiny__rd_example__modalDialog_Rd", "n_calls": 0}

## Edit Examples
(none)
