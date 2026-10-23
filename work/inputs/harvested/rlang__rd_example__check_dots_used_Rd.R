# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: check_dots_used.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 26

suppressPackageStartupMessages(library(rlang))
f <- function(...) {
  check_dots_used()
  g(...)
}

g <- function(x, y, ...) {
  x + y
}
f(x = 1, y = 2)

try(f(x = 1, y = 2, z = 3))

try(f(x = 1, y = 2, 3, 4, 5))

# Use an `error` handler to handle the error differently.
# For instance to demote the error to a warning:
fn <- function(...) {
  check_dots_empty(
    error = function(cnd) {
      warning(cnd)
    }
  )
  "out"
}
fn()