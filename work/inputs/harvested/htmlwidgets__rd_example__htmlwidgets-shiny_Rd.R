# r2py crawler metadata
# package: htmlwidgets
# source_type: rd_example
# topic: htmlwidgets-shiny.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmlwidgets\help
# lines: 11

suppressPackageStartupMessages(library(htmlwidgets))
# shiny output binding for a widget named 'foo'
fooOutput <- function(outputId, width = "100%", height = "400px") {
  htmlwidgets::shinyWidgetOutput(outputId, "foo", width, height)
}

# shiny render function for a widget named 'foo'
renderFoo <- function(expr, env = parent.frame(), quoted = FALSE) {
  if (!quoted) { expr <- substitute(expr) } # force quoted
  htmlwidgets::shinyRenderWidget(expr, fooOutput, env, quoted = TRUE)
}