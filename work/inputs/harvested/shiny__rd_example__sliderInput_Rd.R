# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: sliderInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 22

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {
options(device.ask.default = FALSE)

ui <- fluidPage(
  sliderInput("obs", "Number of observations:",
    min = 0, max = 1000, value = 500
  ),
  plotOutput("distPlot")
)

# Server logic
server <- function(input, output) {
  output$distPlot <- renderPlot({
    hist(rnorm(input$obs))
  })
}

# Complete app with UI and server components
shinyApp(ui, server)
}