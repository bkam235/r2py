---
id: shiny.shinyapp
package: shiny
confidence: tentative
seed: true
created: 2026-07-05
last_review: 2026-07-05
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
- {"r_hash": "ec2ec133", "r_snippet": "shinyApp(ui, server)", "py_snippet": "app = App(app_ui, server)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "f15450ce", "r_snippet": "shinyServer(function(input, output, session) {\n  output$uppercase <- renderText({\n    toupper(input$message)\n  })\n})", "py_snippet": "def server(input, output, session):", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
