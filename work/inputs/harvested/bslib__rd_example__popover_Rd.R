# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: popover.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 32

if (rlang::is_interactive()) withAutoprint({ # examplesIf

popover(
  shiny::actionButton("btn", "A button"),
  "Popover body content...",
  title = "Popover title"
)

library(shiny)
library(bslib)

ui <- page_fixed(
  card(class = "mt-5",
    card_header(
      popover(
        uiOutput("card_title", inline = TRUE),
        title = "Provide a new title",
        textInput("card_title", NULL, "An editable title")
      )
    ),
    "The card body..."
  )
)

server <- function(input, output) {
  output$card_title <- renderUI({
    list(input$card_title, bsicons::bs_icon("pencil-square"))
  })
}

shinyApp(ui, server)
}) # examplesIf