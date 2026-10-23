# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: fillRow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 21

suppressPackageStartupMessages(library(shiny))
# Only run this example in interactive R sessions.
if (interactive()) {

ui <- fillPage(fillRow(
  plotOutput("plotLeft", height = "100%"),
  fillCol(
    plotOutput("plotTopRight", height = "100%"),
    plotOutput("plotBottomRight", height = "100%")
  )
))

server <- function(input, output, session) {
  output$plotLeft <- renderPlot(plot(cars))
  output$plotTopRight <- renderPlot(plot(pressure))
  output$plotBottomRight <- renderPlot(plot(AirPassengers))
}

shinyApp(ui, server)

}