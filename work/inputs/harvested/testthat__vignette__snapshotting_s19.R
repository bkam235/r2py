# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: snapshotting_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\snapshotting.R
# lines: 7

suppressPackageStartupMessages(library(testthat))
try({
test_that("generates actionable error message", {
  path <- withr::local_tempfile(lines = "")
  expect_snapshot(safe_write_lines(letters, path), error = TRUE)
})
})