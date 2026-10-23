# r2py crawler metadata
# package: ellipsis
# source_type: rd_example
# topic: check_dots_used.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ellipsis\help
# lines: 13

suppressPackageStartupMessages(library(ellipsis))
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