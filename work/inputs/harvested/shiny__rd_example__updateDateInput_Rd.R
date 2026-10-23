# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: updateDateInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 23

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  sliderInput("n", "Day of month", 1, 30, 10),
  dateInput("inDate", "Input date")
)

server <- function(input, output, session) {
  observe({
    date <- as.Date(paste0("2013-04-", input$n))
    updateDateInput(session, "inDate",
      label = paste("Date label", input$n),
      value = date,
      min   = date - 3,
      max   = date + 3
    )
  })
}

shinyApp(ui, server)
}