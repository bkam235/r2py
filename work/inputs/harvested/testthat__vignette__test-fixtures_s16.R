# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 14

suppressPackageStartupMessages(library(testthat))
test_that("local_options() only affects a minimal amount of code", {
  withr::local_options(x = 1)
  expect_equal(getOption("x"), 1)

  local({
    withr::local_options(x = 2)
    expect_equal(getOption("x"), 2)
  })

  expect_equal(getOption("x"), 1)
})

getOption("x")