# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: toast.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 36

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

ui <- page_fluid(
  actionButton("show_simple", "Simple Toast"),
  actionButton("show_header", "Toast with Header")
)

server <- function(input, output, session) {
  observeEvent(input$show_simple, {
    show_toast(
      toast(
        "Operation completed successfully!",
        header = "Success",
        type = "success"
      )
    )
  })

  observeEvent(input$show_header, {
    show_toast(
      toast(
        "Your settings have been saved.",
        header = toast_header(
          title = "Settings Updated",
          status = "just now"
        ),
        type = "success"
      )
    )
  })
}

shinyApp(ui, server)
}) # examplesIf