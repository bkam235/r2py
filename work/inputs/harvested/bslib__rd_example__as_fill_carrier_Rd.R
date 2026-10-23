# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: as_fill_carrier.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 20

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)
shinyApp(
  page_fillable(
    # without `as_fill_carrier()`, the plot won't fill the page because
    # `uiOutput()` is neither a fillable container nor a fill item by default.
    as_fill_carrier(uiOutput("ui"))
  ),
  function(input, output) {
    output$ui <- renderUI({
      div(
        class = "bg-info text-white",
        as_fill_item(),
        "A fill item"
      )
    })
  }
)
}) # examplesIf