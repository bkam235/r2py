# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 4

suppressPackageStartupMessages(library(testthat))
expect_df <- function(tbl) {
  expect_s3_class(tbl, "data.frame")
}