# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: passwordInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 17

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  passwordInput("password", "Password:"),
  actionButton("go", "Go"),
  verbatimTextOutput("value")
)
server <- function(input, output) {
  output$value <- renderText({
    req(input$go)
    isolate(input$password)
  })
}
shinyApp(ui, server)
}