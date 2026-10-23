# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: show_toast.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 31

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

ui <- page_fluid(
  actionButton("show_persistent", "Show Persistent Toast"),
  actionButton("hide_persistent", "Hide Toast")
)

server <- function(input, output, session) {
  toast_id <- reactiveVal(NULL)

  observeEvent(input$show_persistent, {
    id <- show_toast(
      toast(
        body = "This toast won't disappear automatically.",
        autohide = FALSE
      )
    )
    toast_id(id)
  })

  observeEvent(input$hide_persistent, {
    req(toast_id())
    hide_toast(toast_id())
    toast_id(NULL)
  })
}

shinyApp(ui, server)
}) # examplesIf