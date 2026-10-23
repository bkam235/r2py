# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: makeReactiveBinding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 13

suppressPackageStartupMessages(library(shiny))
reactiveConsole(TRUE)

a <- 10
makeReactiveBinding("a")

b <- reactive(a * -1)
observe(print(b()))

a <- 20
a <- 30

reactiveConsole(FALSE)