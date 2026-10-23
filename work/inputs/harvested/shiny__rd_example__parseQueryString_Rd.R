# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: parseQueryString.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 22

suppressPackageStartupMessages(library(shiny))
parseQueryString("?foo=1&bar=b%20a%20r")


# Example of usage within a Shiny app
function(input, output, session) {

  output$queryText <- renderText({
    query <- parseQueryString(session$clientData$url_search)

    # Ways of accessing the values
    if (as.numeric(query$foo) == 1) {
      # Do something
    }
    if (query[["bar"]] == "targetstring") {
      # Do something else
    }

    # Return a string with key-value pairs
    paste(names(query), query, sep = "=", collapse=", ")
  })
}