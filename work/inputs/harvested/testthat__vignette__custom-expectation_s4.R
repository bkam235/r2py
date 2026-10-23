# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 14

suppressPackageStartupMessages(library(testthat))
try({
test_that("success", {
  expect_nrow(mtcars, 32)
})

test_that("failure 1", {
  expect_nrow(mtcars, 30)
})

test_that("failure 2", {
  expect_nrow(matrix(1:5), 2)
})
})