# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_integerish.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 6

suppressPackageStartupMessages(library(rlang))
is_integerish(10L)
is_integerish(10.0)
is_integerish(10.0, n = 2)
is_integerish(10.000001)
is_integerish(TRUE)