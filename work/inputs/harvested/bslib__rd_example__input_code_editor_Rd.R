# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: input_code_editor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 21

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

ui <- page_fluid(
  input_code_editor(
    "sql_query",
    value = "SELECT * FROM table",
    language = "sql"
  ),
  verbatimTextOutput("code_output")
)

server <- function(input, output, session) {
  output$code_output <- renderPrint({
    input$sql_query
  })
}

shinyApp(ui, server)
}) # examplesIf