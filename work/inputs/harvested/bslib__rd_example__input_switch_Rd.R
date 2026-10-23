# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: input_switch.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 28

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

ui <- page_fixed(
  title = "Keyboard Settings",
  h2("Keyboard Settings"),
  input_switch("auto_capitalization", "Auto-Capitalization", TRUE),
  input_switch("auto_correction", "Auto-Correction", TRUE),
  input_switch("check_spelling", "Check Spelling", TRUE),
  input_switch("smart_punctuation", "Smart Punctuation"),
  h2("Preview"),
  verbatimTextOutput("preview")
)

server <- function(input, output, session) {
  output$preview <- renderPrint({
    list(
      auto_capitalization = input$auto_capitalization,
      auto_correction = input$auto_correction,
      check_spelling = input$check_spelling,
      smart_punctuation = input$smart_punctuation
    )
  })
}

shinyApp(ui, server)
}) # examplesIf