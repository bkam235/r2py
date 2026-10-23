# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: column.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 38

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  fluidRow(
    column(4,
      sliderInput("obs", "Number of observations:",
                  min = 1, max = 1000, value = 500)
    ),
    column(8,
      plotOutput("distPlot")
    )
  )
)

server <- function(input, output) {
  output$distPlot <- renderPlot({
    hist(rnorm(input$obs))
  })
}

shinyApp(ui, server)



ui <- fluidPage(
  fluidRow(
    column(width = 4,
      "4"
    ),
    column(width = 3, offset = 2,
      "3 offset 2"
    )
  )
)
shinyApp(ui, server = function(input, output) { })
}