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
- {"r_hash": "17d479c6", "r_snippet": "  shinyApp(\n    ui = fluidPage(\n      sidebarLayout(\n        sidebarPanel(\n          p(\"The first slider controls the second\"),\n          sliderInput(\"control\", \"Controller:\", min=0, max=20, value=10,\n                       step=1),\n          sliderInput(\"receive\", \"Receiver:\", min=0, max=20, value=", "py_snippet": "app_ui = ui.page_fluid(\n    ui.layout_sidebar(\n        ui.sidebar(\n            ui.markdown(\"The first slider controls the second\"),\n            ui.input_slider(\"control\", \"Controller:\", min=0, max=20, value=10, step=1),\n            ui.input_slider(\"receive\", \"Receiver:\", min=0, max=20, value=10, step=1),\n        ),\n        # The main panel in layout_sidebar is just the second positional argument.\n        # If empty in R (mainPanel()), we provide an empty div or nothing.\n        ui.div() \n    )\n)\n\ndef server(input, output, session):\n    @reactive.effect\n    def _():\n        val = input.control(", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
