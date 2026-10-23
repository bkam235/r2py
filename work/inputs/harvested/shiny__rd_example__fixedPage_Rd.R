# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: fixedPage.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 18

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fixedPage(
  title = "Hello, Shiny!",
  fixedRow(
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