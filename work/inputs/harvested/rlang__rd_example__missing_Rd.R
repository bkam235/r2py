# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: missing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 9

suppressPackageStartupMessages(library(rlang))
typeof(NA)
typeof(na_lgl)
typeof(na_int)

# Note that while the base R missing symbols cannot be overwritten,
# that's not the case for rlang's aliases:
na_dbl <- NA
typeof(na_dbl)