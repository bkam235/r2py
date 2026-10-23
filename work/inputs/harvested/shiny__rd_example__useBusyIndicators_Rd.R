# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: useBusyIndicators.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 27

suppressPackageStartupMessages(library(shiny))
if (rlang::is_interactive()) withAutoprint({ # examplesIf

library(bslib)

ui <- page_fillable(
  useBusyIndicators(),
  card(
    card_header(
      "A plot",
      input_task_button("simulate", "Simulate"),
      class = "d-flex justify-content-between align-items-center"
    ),
    plotOutput("p"),
  )
)

server <- function(input, output) {
  output$p <- renderPlot({
    input$simulate
    Sys.sleep(4)
    plot(x = rnorm(100), y = rnorm(100))
  })
}

shinyApp(ui, server)
}) # examplesIf