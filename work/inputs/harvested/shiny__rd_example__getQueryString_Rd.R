# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: getQueryString.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 52

suppressPackageStartupMessages(library(shiny))
## Only run this example in interactive R sessions
if (interactive()) {

  ## App 1: getQueryString
  ## Printing the value of the query string
  ## (Use the back and forward buttons to see how the browser
  ## keeps a record of each state)
  shinyApp(
    ui = fluidPage(
      textInput("txt", "Enter new query string"),
      helpText("Format: ?param1=val1&param2=val2"),
      actionButton("go", "Update"),
      hr(),
      verbatimTextOutput("query")
    ),
    server = function(input, output, session) {
      observeEvent(input$go, {
        updateQueryString(input$txt, mode = "push")
      })
      output$query <- renderText({
        query <- getQueryString()
        queryText <- paste(names(query), query,
                       sep = "=", collapse=", ")
        paste("Your query string is:\n", queryText)
      })
    }
  )

  ## App 2: getUrlHash
  ## Printing the value of the URL hash
  ## (Use the back and forward buttons to see how the browser
  ## keeps a record of each state)
  shinyApp(
    ui = fluidPage(
      textInput("txt", "Enter new hash"),
      helpText("Format: #hash"),
      actionButton("go", "Update"),
      hr(),
      verbatimTextOutput("hash")
    ),
    server = function(input, output, session) {
      observeEvent(input$go, {
        updateQueryString(input$txt, mode = "push")
      })
      output$hash <- renderText({
        hash <- getUrlHash()
        paste("Your hash is:\n", hash)
      })
    }
  )
}