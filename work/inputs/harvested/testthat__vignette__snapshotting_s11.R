# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: snapshotting_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\snapshotting.R
# lines: 6

suppressPackageStartupMessages(library(testthat))
try({
test_that("you can't add a number and a letter", {
  expect_snapshot(1 + "a")
})
})