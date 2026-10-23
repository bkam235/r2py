# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: req.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 24

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {
  ui <- fluidPage(
    textInput('data', 'Enter a dataset from the "datasets" package', 'cars'),
    p('(E.g. "cars", "mtcars", "pressure", "faithful")'), hr(),
    tableOutput('tbl')
  )

  server <- function(input, output) {
    output$tbl <- renderTable({

      ## to require that the user types something, use: `req(input$data)`
      ## but better: require that input$data is valid and leave the last
      ## valid table up
      req(exists(input$data, "package:datasets", inherits = FALSE),
          cancelOutput = TRUE)

      head(get(input$data, "package:datasets", inherits = FALSE))
    })
  }

  shinyApp(ui, server)
}