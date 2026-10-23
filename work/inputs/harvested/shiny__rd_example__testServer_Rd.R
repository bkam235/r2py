# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: testServer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 37

suppressPackageStartupMessages(library(shiny))
# Testing a server function  ----------------------------------------------
server <- function(input, output, session) {
  x <- reactive(input$a * input$b)
}

testServer(server, {
  session$setInputs(a = 2, b = 3)
  stopifnot(x() == 6)
})


# Testing a module --------------------------------------------------------
myModuleServer <- function(id, multiplier = 2, prefix = "I am ") {
  moduleServer(id, function(input, output, session) {
    myreactive <- reactive({
      input$x * multiplier
    })
    output$txt <- renderText({
      paste0(prefix, myreactive())
    })
  })
}

testServer(myModuleServer, args = list(multiplier = 2), {
  session$setInputs(x = 1)
  # You're also free to use third-party
  # testing packages like testthat:
  #   expect_equal(myreactive(), 2)
  stopifnot(myreactive() == 2)
  stopifnot(output$txt == "I am 2")

  session$setInputs(x = 2)
  stopifnot(myreactive() == 4)
  stopifnot(output$txt == "I am 4")
  # Any additional arguments, below, are passed along to the module.
})