# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: titlePanel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 9

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  titlePanel("Hello Shiny!")
)
shinyApp(ui, server = function(input, output) { })
}