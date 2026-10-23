# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: check_dots_unnamed.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 9

suppressPackageStartupMessages(library(rlang))
f <- function(..., foofy = 8) {
  check_dots_unnamed()
  c(...)
}

f(1, 2, 3, foofy = 4)

try(f(1, 2, 3, foof = 4))