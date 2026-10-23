# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: getCurrentOutputInfo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 36

suppressPackageStartupMessages(library(shiny))
if (interactive()) {
  shinyApp(
    fluidPage(
      tags$style(HTML("body {background-color: black; color: white; }")),
      tags$style(HTML("body a {color: purple}")),
      tags$style(HTML("#info {background-color: teal; color: orange; }")),
      plotOutput("p"),
      "Computed CSS styles for the output named info:",
      tagAppendAttributes(
        textOutput("info"),
        class = "shiny-report-theme"
      )
    ),
    function(input, output) {
      output$p <- renderPlot({
        info <- getCurrentOutputInfo()
        par(bg = info$bg(), fg = info$fg(), col.axis = info$fg(), col.main = info$fg())
        plot(1:10, col = info$accent(), pch = 19)
        title("A simple R plot that uses its CSS styling")
      })
      output$info <- renderText({
        info <- getCurrentOutputInfo()
        jsonlite::toJSON(
          list(
            bg = info$bg(),
            fg = info$fg(),
            accent = info$accent(),
            font = info$font()
          ),
          auto_unbox = TRUE
        )
      })
    }
  )
}