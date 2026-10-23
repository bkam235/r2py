# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: capture_output.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 13

suppressPackageStartupMessages(library(testthat))
capture_output({
  cat("Hi!\n")
  cat("Bye\n")
})

capture_output_lines({
  cat("Hi!\n")
  cat("Bye\n")
})

capture_output("Hi")
capture_output("Hi", print = TRUE)