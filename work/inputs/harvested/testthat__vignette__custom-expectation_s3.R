# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 6

suppressPackageStartupMessages(library(testthat))
# from tidytext
expect_nrow <- function(tbl, n) {
  expect_s3_class(tbl, "data.frame")
  expect_equal(nrow(tbl), n)
}