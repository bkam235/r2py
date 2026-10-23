# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 8

suppressPackageStartupMessages(library(testthat))
test_that("can print one digit of pi", {
  op <- options(digits = 1)
  on.exit(options(op), add = TRUE, after = FALSE)
  
  expect_output(print(pi), "3")
})
pi