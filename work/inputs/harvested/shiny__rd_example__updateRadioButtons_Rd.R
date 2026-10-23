# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateRadioButtons.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 27

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  p("The first radio button group controls the second"),
  radioButtons("inRadioButtons", "Input radio buttons",
    c("Item A", "Item B", "Item C")),
  radioButtons("inRadioButtons2", "Input radio buttons 2",
    c("Item A", "Item B", "Item C"))
)

server <- function(input, output, session) {
  observe({
    x <- input$inRadioButtons

    # Can also set the label and select items
    updateRadioButtons(session, "inRadioButtons2",
      label = paste("radioButtons label", x),
      choices = x,
      selected = x
    )
  })
}

shinyApp(ui, server)
}