# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 7

suppressPackageStartupMessages(library(testthat))
message3 <- function(..., verbose = getOption("verbose")) {
  if (!isTRUE(verbose)) {
    return()
  }
  message(...)
}