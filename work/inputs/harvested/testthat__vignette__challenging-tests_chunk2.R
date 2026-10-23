# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: challenging-tests_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\challenging-tests.Rmd
# lines: 13

suppressPackageStartupMessages(library(testthat))
#| label: random-local-seed
dice <- function() {
  sample(6, 1)
}

test_that("dice returns different numbers", {
  withr::local_seed(1234)

  expect_equal(dice(), 4)
  expect_equal(dice(), 2)
  expect_equal(dice(), 6)
})