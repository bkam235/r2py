# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: shinyServer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 18

suppressPackageStartupMessages(library(shiny))
# A very simple Shiny app that takes a message from the user
# and outputs an uppercase version of it.
shinyServer(function(input, output, session) {
  output$uppercase <- renderText({
    toupper(input$message)
  })
})


# It is also possible for a server.R file to simply return the function,
# without calling shinyServer().
# For example, the server.R file could contain just the following:
function(input, output, session) {
  output$uppercase <- renderText({
    toupper(input$message)
  })
}