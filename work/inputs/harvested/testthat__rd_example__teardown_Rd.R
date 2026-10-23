# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: teardown.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 16

suppressPackageStartupMessages(library(testthat))
# Old approach
tmp <- tempfile()
setup(writeLines("some test data", tmp))
teardown(unlink(tmp))


# Now recommended:
local_test_data <- function(env = parent.frame()) {
  tmp <- tempfile()
  writeLines("some test data", tmp)
  withr::defer(unlink(tmp), env)

  tmp
}
# Then call local_test_data() in your tests