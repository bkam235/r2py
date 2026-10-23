# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_error.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 42

suppressPackageStartupMessages(library(testthat))
# Errors ------------------------------------------------------------------
f <- function() stop("My error!")
expect_error(f())
expect_error(f(), "My error!")

# You can use the arguments of grepl to control the matching
expect_error(f(), "my error!", ignore.case = TRUE)

# Note that `expect_error()` returns the error object so you can test
# its components if needed
err <- expect_error(rlang::abort("a", n = 10))
expect_equal(err$n, 10)

# Warnings ------------------------------------------------------------------
f <- function(x) {
  if (x < 0) {
    warning("*x* is already negative")
    return(x)
  }
  -x
}
expect_warning(f(-1))
expect_warning(f(-1), "already negative")
expect_warning(f(1), NA)

# To test message and output, store results to a variable
expect_warning(out <- f(-1), "already negative")
expect_equal(out, -1)

# Messages ------------------------------------------------------------------
f <- function(x) {
  if (x < 0) {
    message("*x* is already negative")
    return(x)
  }

  -x
}
expect_message(f(-1))
expect_message(f(-1), "already negative")
expect_message(f(1), NA)