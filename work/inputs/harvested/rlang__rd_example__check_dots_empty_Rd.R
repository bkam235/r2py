# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: check_dots_empty.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 14

suppressPackageStartupMessages(library(rlang))
f <- function(x, ..., foofy = 8) {
  check_dots_empty()
  x + foofy
}

# This fails because `foofy` can't be matched positionally
try(f(1, 4))

# This fails because `foofy` can't be matched partially by name
try(f(1, foof = 4))

# Thanks to `...`, it must be matched exactly
f(1, foofy = 4)