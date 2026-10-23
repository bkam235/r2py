# r2py crawler metadata
# package: miniUI
# source_type: rd_example
# topic: miniTabstripPanel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\miniUI\help
# lines: 10

suppressPackageStartupMessages(library(miniUI))
library(shiny)

miniTabstripPanel(
  miniTabPanel("Data", icon = icon("table"),
    selectInput("dataset", "Data set", ls("package:datasets"))),
  miniTabPanel("Subset", icon = icon("sliders"),
    uiOutput("subset_ui")
  )
)