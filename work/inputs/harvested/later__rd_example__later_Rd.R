# r2py crawler metadata
# package: later
# source_type: rd_example
# topic: later.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\later\help
# lines: 8

suppressPackageStartupMessages(library(later))
# Example of formula style
later(~cat("Hello from the past\n"), 3)

# Example of function style
later(function() {
  print(summary(cars))
}, 2)