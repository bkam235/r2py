# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateDateRangeInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 25

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  sliderInput("n", "Day of month", 1, 30, 10),
  dateRangeInput("inDateRange", "Input date range")
)

server <- function(input, output, session) {
  observe({
    date <- as.Date(paste0("2013-04-", input$n))

    updateDateRangeInput(session, "inDateRange",
      label = paste("Date range label", input$n),
      start = date - 1,
      end = date + 1,
      min = date - 5,
      max = date + 5
    )
  })
}

shinyApp(ui, server)
}