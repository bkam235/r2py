# r2py crawler metadata
# package: miniUI
# source_type: rd_example
# topic: miniContentPanel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\miniUI\help
# lines: 6

suppressPackageStartupMessages(library(miniUI))
library(shiny)

miniContentPanel(padding = 0,
  plotOutput("plot", height = "100%")
)