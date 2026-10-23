# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: local_test_context.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 14

suppressPackageStartupMessages(library(testthat))
local({
  local_test_context()
  cat(cli::col_blue("Text will not be colored"))
  cat(cli::symbol$ellipsis)
  cat("\n")
})
test_that("test ellipsis", {
  local_reproducible_output(unicode = FALSE)
  expect_equal(cli::symbol$ellipsis, "...")

  local_reproducible_output(unicode = TRUE)
  expect_equal(cli::symbol$ellipsis, "\u2026")
})