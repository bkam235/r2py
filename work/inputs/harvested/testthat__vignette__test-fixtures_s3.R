# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 10

suppressPackageStartupMessages(library(testthat))
test_that("print() respects digits option", {
  x <- 1.23456789

  withr::local_options(digits = 1)
  expect_equal(capture.output(x), "[1] 1")

  withr::local_options(digits = 5)
  expect_equal(capture.output(x), "[1] 1.2346")
})