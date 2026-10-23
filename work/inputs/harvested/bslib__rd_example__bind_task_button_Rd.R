# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: bind_task_button.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 39

if (rlang::is_interactive()) withAutoprint({ # examplesIf

library(shiny)
library(bslib)
library(future)
plan(multisession)

ui <- page_sidebar(
  sidebar = sidebar(
    input_task_button("recalc", "Recalculate")
  ),
  textOutput("outval")
)

server <- function(input, output) {
  rand_task <- ExtendedTask$new(function() {
    future({
      # Slow operation goes here
      Sys.sleep(2)
      runif(1)
    }, seed = TRUE)
  })

  # Make button state reflect task.
  # If using R >=4.1, you can do this instead:
  # rand_task <- ExtendedTask$new(...) |> bind_task_button("recalc")
  bind_task_button(rand_task, "recalc")

  observeEvent(input$recalc, {
    rand_task$invoke()
  })

  output$outval <- renderText({
    rand_task$result()
  })
}

shinyApp(ui, server)
}) # examplesIf