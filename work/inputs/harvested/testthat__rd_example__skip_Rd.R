# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: skip.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 9

suppressPackageStartupMessages(library(testthat))
if (FALSE) skip("Some Important Requirement is not available")

test_that("skip example", {
  expect_equal(1, 1L)    # this expectation runs
  skip('skip')
  expect_equal(1, 2)     # this one skipped
  expect_equal(1, 3)     # this one is also skipped
})