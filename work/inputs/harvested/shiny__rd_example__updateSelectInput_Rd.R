# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateSelectInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 31

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  p("The checkbox group controls the select input"),
  checkboxGroupInput("inCheckboxGroup", "Input checkbox",
    c("Item A", "Item B", "Item C")),
  selectInput("inSelect", "Select input",
    c("Item A", "Item B", "Item C"))
)

server <- function(input, output, session) {
  observe({
    x <- input$inCheckboxGroup

    # Can use character(0) to remove all choices
    if (is.null(x))
      x <- character(0)

    # Can also set the label and select items
    updateSelectInput(session, "inSelect",
      label = paste("Select input label", length(x)),
      choices = x,
      selected = tail(x, 1)
    )
  })
}

shinyApp(ui, server)
}