# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_no_error.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 12

suppressPackageStartupMessages(library(testthat))
expect_no_warning(1 + 1)

foo <- function(x) {
  warning("This is a problem!")
}

# warning doesn't match so bubbles up:
expect_no_warning(foo(), message = "bananas")

# warning does match so causes a failure:
try(expect_no_warning(foo(), message = "problem"))