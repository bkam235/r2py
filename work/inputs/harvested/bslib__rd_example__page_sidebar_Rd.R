# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: page_sidebar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 26

if (rlang::is_interactive()) withAutoprint({ # examplesIf

library(shiny)
library(ggplot2)
library(bslib)

ui <- page_sidebar(
  title = "Example dashboard",
  sidebar = sidebar(
    varSelectInput("var", "Select variable", mtcars)
  ),
  card(
    full_screen = TRUE,
    card_header("My plot"),
    plotOutput("p")
  )
)

server <- function(input, output) {
  output$p <- renderPlot({
    ggplot(mtcars) + geom_histogram(aes(!!input$var))
  })
}

shinyApp(ui, server)
}) # examplesIf