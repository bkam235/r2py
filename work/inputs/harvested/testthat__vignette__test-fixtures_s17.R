# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 7

suppressPackageStartupMessages(library(testthat))
message2 <- function(...) {
  if (!isTRUE(getOption("verbose"))) {
    return()
  }
  message(...)
}