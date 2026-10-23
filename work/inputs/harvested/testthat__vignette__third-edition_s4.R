# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: third-edition_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\third-edition.R
# lines: 5

suppressPackageStartupMessages(library(testthat))
test_that("I want to use the 2nd edition", {
  local_edition(2)
  expect_true(TRUE)
})