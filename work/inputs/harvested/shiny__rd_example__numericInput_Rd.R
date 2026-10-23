# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: numericInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 13

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  numericInput("obs", "Observations:", 10, min = 1, max = 100),
  verbatimTextOutput("value")
)
server <- function(input, output) {
  output$value <- renderText({ input$obs })
}
shinyApp(ui, server)
}