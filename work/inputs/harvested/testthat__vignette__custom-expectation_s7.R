# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 11

suppressPackageStartupMessages(library(testthat))
test_that("expect_length works as expected", {
  x <- 1:10
  expect_success(expect_length(x, 10))
  expect_failure(expect_length(x, 11))
})

test_that("expect_length gives useful feedback", {
  x <- 1:10
  expect_snapshot_failure(expect_length(x, 11))
})