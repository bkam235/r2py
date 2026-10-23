# r2py crawler metadata
# package: lifecycle
# source_type: rd_example
# topic: verbosity.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\help
# lines: 23

suppressPackageStartupMessages(library(lifecycle))
if (rlang::is_installed("testthat")) {
  library(testthat)

  mytool <- function() {
    deprecate_soft("1.0.0", "mytool()")
    10 * 10
  }

  # Forcing the verbosity level is useful for unit testing. You can
  # force errors to test that the function is indeed deprecated:
  test_that("mytool is deprecated", {
    rlang::local_options(lifecycle_verbosity = "error")
    expect_error(mytool(), class = "defunctError")
  })

  # Or you can enforce silence to safely test that the function
  # still works:
  test_that("mytool still works", {
    rlang::local_options(lifecycle_verbosity = "quiet")
    expect_equal(mytool(), 100)
  })
}