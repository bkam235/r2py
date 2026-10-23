# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: fillPage.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 22

suppressPackageStartupMessages(library(shiny))
fillPage(
  tags$style(type = "text/css",
    ".half-fill { width: 50%; height: 100%; }",
    "#one { float: left; background-color: #ddddff; }",
    "#two { float: right; background-color: #ccffcc; }"
  ),
  div(id = "one", class = "half-fill",
    "Left half"
  ),
  div(id = "two", class = "half-fill",
    "Right half"
  ),
  padding = 10
)

fillPage(
  fillRow(
    div(style = "background-color: red; width: 100%; height: 100%;"),
    div(style = "background-color: blue; width: 100%; height: 100%;")
  )
)