# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: withProgressShiny.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 35

library(shiny)
library(progressr)

app <- shinyApp(
  ui = fluidPage(
    plotOutput("plot")
  ),

  server = function(input, output) {
    output$plot <- renderPlot({
      X <- 1:15
      withProgressShiny(message = "Calculation in progress",
                        detail = "Starting ...",
                        value = 0, {
        p <- progressor(along = X)
        y <- lapply(X, FUN=function(x) {
          Sys.sleep(0.25)
          p(sprintf("x=%d", x))
        })
      })
      
      plot(cars)

      ## Terminate the Shiny app
      Sys.sleep(1.0)
      stopApp(returnValue = invisible())
    })
  }
)

local({
  oopts <- options(device.ask.default = FALSE)
  on.exit(options(oopts))
  if (interactive()) print(app)
})