# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: freezeReactiveValue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 35

suppressPackageStartupMessages(library(shiny))
## Only run this examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  selectInput("data", "Data Set", c("mtcars", "pressure")),
  checkboxGroupInput("cols", "Columns (select 2)", character(0)),
  plotOutput("plot")
)

server <- function(input, output, session) {
  observe({
    data <- get(input$data)
    # Sets a flag on input$cols to essentially do req(FALSE) if input$cols
    # is accessed. Without this, an error will momentarily show whenever a
    # new data set is selected.
    freezeReactiveValue(input, "cols")
    updateCheckboxGroupInput(session, "cols", choices = names(data))
  })

  output$plot <- renderPlot({
    # When a new data set is selected, input$cols will have been invalidated
    # above, and this will essentially do the same as req(FALSE), causing
    # this observer to stop and raise a silent exception.
    cols <- input$cols
    data <- get(input$data)

    if (length(cols) == 2) {
      plot(data[[ cols[1] ]], data[[ cols[2] ]])
    }
  })
}

shinyApp(ui, server)
}