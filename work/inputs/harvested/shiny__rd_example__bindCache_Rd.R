# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: bindCache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 91

suppressPackageStartupMessages(library(shiny))
rc <- bindCache(
  x = reactive({
    Sys.sleep(2)   # Pretend this is expensive
    input$x * 100
  }),
  input$x
)

# Can make it prettier with the %>% operator
library(magrittr)

rc <- reactive({
  Sys.sleep(2)
  input$x * 100
}) %>%
  bindCache(input$x)



## Only run app examples in interactive R sessions
if (interactive()) {

# Basic example
shinyApp(
  ui = fluidPage(
    sliderInput("x", "x", 1, 10, 5),
    sliderInput("y", "y", 1, 10, 5),
    div("x * y: "),
    verbatimTextOutput("txt")
  ),
  server = function(input, output) {
    r <- reactive({
      # The value expression is an _expensive_ computation
      message("Doing expensive computation...")
      Sys.sleep(2)
      input$x * input$y
    }) %>%
      bindCache(input$x, input$y)

    output$txt <- renderText(r())
  }
)


# Caching renderText
shinyApp(
  ui = fluidPage(
    sliderInput("x", "x", 1, 10, 5),
    sliderInput("y", "y", 1, 10, 5),
    div("x * y: "),
    verbatimTextOutput("txt")
  ),
  server = function(input, output) {
    output$txt <- renderText({
      message("Doing expensive computation...")
      Sys.sleep(2)
      input$x * input$y
    }) %>%
      bindCache(input$x, input$y)
  }
)


# Demo of using events and caching with an actionButton
shinyApp(
  ui = fluidPage(
    sliderInput("x", "x", 1, 10, 5),
    sliderInput("y", "y", 1, 10, 5),
    actionButton("go", "Go"),
    div("x * y: "),
    verbatimTextOutput("txt")
  ),
  server = function(input, output) {
    r <- reactive({
      message("Doing expensive computation...")
      Sys.sleep(2)
      input$x * input$y
    }) %>%
      bindCache(input$x, input$y) %>%
      bindEvent(input$go)
      # The cached, eventified reactive takes a reactive dependency on
      # input$go, but doesn't use it for the cache key. It uses input$x and
      # input$y for the cache key, but doesn't take a reactive dependency on
      # them, because the reactive dependency is superseded by addEvent().

    output$txt <- renderText(r())
  }
)

}