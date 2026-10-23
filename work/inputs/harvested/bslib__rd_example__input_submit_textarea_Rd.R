# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: input_submit_textarea.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 17

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

ui <- page_fluid(
  input_submit_textarea("text", placeholder = "Enter some input..."),
  verbatimTextOutput("value")
)
server <- function(input, output) {
  output$value <- renderText({
    req(input$text)
    Sys.sleep(2)
    paste("You entered:", input$text)
  })
}
shinyApp(ui, server)
}) # examplesIf