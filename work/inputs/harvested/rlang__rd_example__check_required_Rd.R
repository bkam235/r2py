# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: check_required.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 10

suppressPackageStartupMessages(library(rlang))
f <- function(x)  {
  check_required(x)
}

# Fails because `x` is not supplied
try(f())

# Succeeds
f(NULL)