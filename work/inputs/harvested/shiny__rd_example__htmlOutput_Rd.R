# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: htmlOutput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 7

suppressPackageStartupMessages(library(shiny))
htmlOutput("summary")

# Using a custom container and class
tags$ul(
  htmlOutput("summary", container = tags$li, class = "custom-li-output")
)