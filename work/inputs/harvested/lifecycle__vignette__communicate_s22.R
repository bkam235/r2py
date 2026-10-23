# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 11

suppressPackageStartupMessages(library(lifecycle))
add_two <- function(x, y) {
  if (length(y) != 1) {
    lifecycle::deprecate_warn("1.0.0", "foo(y = 'must be a scalar')")
    y <- sum(y)
  }
  x + y
}

add_two(1, 2)
add_two(1, 1:5)