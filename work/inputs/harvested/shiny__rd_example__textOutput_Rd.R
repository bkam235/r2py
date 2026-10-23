# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: textOutput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 15

suppressPackageStartupMessages(library(shiny))
## Only run this example in interactive R sessions
if (interactive()) {
  shinyApp(
    ui = basicPage(
      textInput("txt", "Enter the text to display below:"),
      textOutput("text"),
      verbatimTextOutput("verb")
    ),
    server = function(input, output) {
      output$text <- renderText({ input$txt })
      output$verb <- renderText({ input$txt })
    }
  )
}