# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: input_task_button.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 25

if (interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

ui <- page_sidebar(
  sidebar = sidebar(
    open = "always",
    input_task_button("resample", "Resample"),
  ),
  verbatimTextOutput("summary")
)

server <- function(input, output, session) {
  sample <- eventReactive(input$resample, ignoreNULL=FALSE, {
    Sys.sleep(2)  # Make this artificially slow
    rnorm(100)
  })

  output$summary <- renderPrint({
    summary(sample())
  })
}

shinyApp(ui, server)
}) # examplesIf