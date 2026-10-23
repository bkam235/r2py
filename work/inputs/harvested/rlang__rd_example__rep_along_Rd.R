# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: rep_along.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
x <- 0:5
rep_along(x, 1:2)
rep_along(x, 1)

# Create fresh vectors by repeating missing values:
rep_along(x, na_int)
rep_along(x, na_chr)

# rep_named() repeats a value along a names vectors
rep_named(c("foo", "bar"), list(letters))