# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: verticalLayout.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 13

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  verticalLayout(
    a(href="http://example.com/link1", "Link One"),
    a(href="http://example.com/link2", "Link Two"),
    a(href="http://example.com/link3", "Link Three")
  )
)
shinyApp(ui, server = function(input, output) { })
}