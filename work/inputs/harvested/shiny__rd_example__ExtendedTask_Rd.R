# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: ExtendedTask.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 50

if (rlang::is_interactive() && rlang::is_installed("mirai")) withAutoprint({ # examplesIf
library(shiny)
library(bslib)
library(mirai)

# Set background processes for running tasks
daemons(1)
# Reset when the app is stopped
onStop(function() daemons(0))

ui <- page_fluid(
  titlePanel("Extended Task Demo"),
  p(
    'Click the button below to perform a "calculation"',
    "that takes a while to perform."
  ),
  input_task_button("recalculate", "Recalculate"),
  p(textOutput("result"))
)

server <- function(input, output) {
  rand_task <- ExtendedTask$new(function() {
    mirai(
      {
        # Slow operation goes here
        Sys.sleep(2)
        sample(1:100, 1)
      }
    )
  })

  # Make button state reflect task.
  # If using R >=4.1, you can do this instead:
  # rand_task <- ExtendedTask$new(...) |> bind_task_button("recalculate")
  bind_task_button(rand_task, "recalculate")

  observeEvent(input$recalculate, {
    # Invoke the extended in an observer
    rand_task$invoke()
  })

  output$result <- renderText({
    # React to updated results when the task completes
    number <- rand_task$result()
    paste0("Your number is ", number, ".")
  })
}

shinyApp(ui, server)
}) # examplesIf