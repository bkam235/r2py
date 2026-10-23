# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: moduleServer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 70

suppressPackageStartupMessages(library(shiny))
# Define the UI for a module
counterUI <- function(id, label = "Counter") {
  ns <- NS(id)
  tagList(
    actionButton(ns("button"), label = label),
    verbatimTextOutput(ns("out"))
  )
}

# Define the server logic for a module
counterServer <- function(id) {
  moduleServer(
    id,
    function(input, output, session) {
      count <- reactiveVal(0)
      observeEvent(input$button, {
        count(count() + 1)
      })
      output$out <- renderText({
        count()
      })
      count
    }
  )
}

# Use the module in an app
ui <- fluidPage(
  counterUI("counter1", "Counter #1"),
  counterUI("counter2", "Counter #2")
)
server <- function(input, output, session) {
  counterServer("counter1")
  counterServer("counter2")
}
if (interactive()) {
  shinyApp(ui, server)
}



# If you want to pass extra parameters to the module's server logic, you can
# add them to your function. In this case `prefix` is text that will be
# printed before the count.
counterServer2 <- function(id, prefix = NULL) {
  moduleServer(
    id,
    function(input, output, session) {
      count <- reactiveVal(0)
      observeEvent(input$button, {
        count(count() + 1)
      })
      output$out <- renderText({
        paste0(prefix, count())
      })
      count
    }
  )
}

ui <- fluidPage(
  counterUI("counter", "Counter"),
)
server <- function(input, output, session) {
  counterServer2("counter", "The current count is: ")
}
if (interactive()) {
  shinyApp(ui, server)
}