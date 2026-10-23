# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: capture_condition.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 15

suppressPackageStartupMessages(library(testthat))
f <- function() {
  message("First")
  warning("Second")
  message("Third")
}

capture_message(f())
capture_messages(f())

capture_warning(f())
capture_warnings(f())

# Condition will capture anything
capture_condition(f())