# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: fail.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 13

suppressPackageStartupMessages(library(testthat))
expect_length <- function(object, n) {
  act <- quasi_label(rlang::enquo(object), arg = "object")

  act_n <- length(act$val)
  if (act_n != n) {
    fail(sprintf("%s has length %i, not length %i.", act$lab, act_n, n))
  } else {
    pass()
  }

  invisible(act$val)
}