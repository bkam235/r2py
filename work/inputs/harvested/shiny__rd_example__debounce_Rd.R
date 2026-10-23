# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: debounce.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 38

## Only run examples in interactive R sessions
if (interactive()) {
options(device.ask.default = FALSE)

library(shiny)
library(magrittr)

ui <- fluidPage(
  plotOutput("plot", click = clickOpts("hover")),
  helpText("Quickly click on the plot above, while watching the result table below:"),
  tableOutput("result")
)

server <- function(input, output, session) {
  hover <- reactive({
    if (is.null(input$hover))
      list(x = NA, y = NA)
    else
      input$hover
  })
  hover_d <- hover %>% debounce(1000)
  hover_t <- hover %>% throttle(1000)

  output$plot <- renderPlot({
    plot(cars)
  })

  output$result <- renderTable({
    data.frame(
      mode = c("raw", "throttle", "debounce"),
      x = c(hover()$x, hover_t()$x, hover_d()$x),
      y = c(hover()$y, hover_t()$y, hover_d()$y)
    )
  })
}

shinyApp(ui, server)
}