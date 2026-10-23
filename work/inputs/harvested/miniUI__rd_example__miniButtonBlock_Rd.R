# r2py crawler metadata
# package: miniUI
# source_type: rd_example
# topic: miniButtonBlock.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\miniUI\help
# lines: 7

suppressPackageStartupMessages(library(miniUI))
library(shiny)

miniButtonBlock(
  actionButton("reset", "Reset to defaults"),
  actionButton("clear", "Clear all")
)