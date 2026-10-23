# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: reactiveFileReader.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 19

suppressPackageStartupMessages(library(shiny))
# Per-session reactive file reader
function(input, output, session) {
  fileData <- reactiveFileReader(1000, session, 'data.csv', read.csv)

  output$data <- renderTable({
    fileData()
  })
}

# Cross-session reactive file reader. In this example, all sessions share
# the same reader, so read.csv only gets executed once no matter how many
# user sessions are connected.
fileData <- reactiveFileReader(1000, NULL, 'data.csv', read.csv)
function(input, output, session) {
  output$data <- renderTable({
    fileData()
  })
}