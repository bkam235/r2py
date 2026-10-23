# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: reactiveConsole.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 9

suppressPackageStartupMessages(library(shiny))
reactiveConsole(TRUE)
x <- reactiveVal(10)
y <- observe({
  message("The value of x is ", x())
})
x(20)
x(30)
reactiveConsole(FALSE)