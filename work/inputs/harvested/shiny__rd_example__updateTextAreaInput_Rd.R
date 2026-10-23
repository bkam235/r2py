# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateTextAreaInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 28

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  sliderInput("controller", "Controller", 0, 20, 10),
  textAreaInput("inText", "Input textarea"),
  textAreaInput("inText2", "Input textarea 2")
)

server <- function(input, output, session) {
  observe({
    # We'll use the input$controller variable multiple times, so save it as x
    # for convenience.
    x <- input$controller

    # This will change the value of input$inText, based on x
    updateTextAreaInput(session, "inText", value = paste("New text", x))

    # Can also set the label, this time for input$inText2
    updateTextAreaInput(session, "inText2",
      label = paste("New label", x),
      value = paste("New text", x))
  })
}

shinyApp(ui, server)
}