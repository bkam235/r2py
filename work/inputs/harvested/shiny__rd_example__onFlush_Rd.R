# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: onFlush.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 48

if (interactive()) withAutoprint({ # examplesIf
library(shiny)

ui <- fixedPage(
  markdown(c(
    "Set the number to 8 or higher to cause an error",
    "in the `renderText()` output."
  )),
  sliderInput("number", "Number", 0, 10, 4),
  textOutput("text"),
  hr(),
  markdown(c(
    "Click the button below to crash the app with an unhandled error",
    "in an `observe()` block."
  )),
  actionButton("crash", "Crash the app!")
)

log_event <- function(level, ...) {
  ts <- strftime(Sys.time(), " [%F %T] ")
  message(level, ts, ...)
}

server <- function(input, output, session) {
  log_event("INFO", "Session started")

  onUnhandledError(function(err) {
    # log the unhandled error
    level <- if (inherits(err, "shiny.error.fatal")) "FATAL" else "ERROR"
    log_event(level, conditionMessage(err))
  })

  onStop(function() {
    log_event("INFO", "Session ended")
  })

  observeEvent(input$crash, stop("Oops, an unhandled error happened!"))

  output$text <- renderText({
    if (input$number > 7) {
      stop("that's too high!")
    }
    sprintf("You picked number %d.", input$number)
  })
}

shinyApp(ui, server)
}) # examplesIf