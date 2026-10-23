# r2py crawler metadata
# package: ellipsis
# source_type: rd_example
# topic: check_dots_empty.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ellipsis\help
# lines: 8

suppressPackageStartupMessages(library(ellipsis))
f <- function(x, ..., foofy = 8) {
  check_dots_empty()
  x + foofy
}

try(f(1, foof = 4))
f(1, foofy = 4)