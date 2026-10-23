# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: navlistPanel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 12

suppressPackageStartupMessages(library(shiny))
fluidPage(

  titlePanel("Application Title"),

  navlistPanel(
    "Header",
    tabPanel("First"),
    tabPanel("Second"),
    tabPanel("Third")
  )
)