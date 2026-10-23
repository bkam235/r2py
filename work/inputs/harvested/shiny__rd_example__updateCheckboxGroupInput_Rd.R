# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateCheckboxGroupInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 31

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  p("The first checkbox group controls the second"),
  checkboxGroupInput("inCheckboxGroup", "Input checkbox",
    c("Item A", "Item B", "Item C")),
  checkboxGroupInput("inCheckboxGroup2", "Input checkbox 2",
    c("Item A", "Item B", "Item C"))
)

server <- function(input, output, session) {
  observe({
    x <- input$inCheckboxGroup

    # Can use character(0) to remove all choices
    if (is.null(x))
      x <- character(0)

    # Can also set the label and select items
    updateCheckboxGroupInput(session, "inCheckboxGroup2",
      label = paste("Checkboxgroup label", length(x)),
      choices = x,
      selected = x
    )
  })
}

shinyApp(ui, server)
}