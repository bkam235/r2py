# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateCheckboxInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 20

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  sliderInput("controller", "Controller", 0, 1, 0, step = 1),
  checkboxInput("inCheckbox", "Input checkbox")
)

server <- function(input, output, session) {
  observe({
    # TRUE if input$controller is odd, FALSE if even.
    x_even <- input$controller %% 2 == 1

    updateCheckboxInput(session, "inCheckbox", value = x_even)
  })
}

shinyApp(ui, server)
}