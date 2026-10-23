# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: checkboxInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 13

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  checkboxInput("somevalue", "Some value", FALSE),
  verbatimTextOutput("value")
)
server <- function(input, output) {
  output$value <- renderText({ input$somevalue })
}
shinyApp(ui, server)
}