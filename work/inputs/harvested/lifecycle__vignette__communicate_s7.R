# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 7

suppressPackageStartupMessages(library(lifecycle))
add_two <- function(x, y) {
  lifecycle::deprecate_warn("1.0.0", "add_two()", "base::sum()")
  x + y
}

add_two(1, 2)