# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s47
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 9

suppressPackageStartupMessages(library(bit))
# TODO(r-lib/lintr#773): nolint as a chunk option.
# nolint start: any_duplicated_linter.
x <- c(NA, NA, 1L, 1L, 2L, 3L)
any(duplicated(x))      # full hash work, returns FALSE or TRUE
anyDuplicated(x)        # early termination of hash work, returns 0 or position of first duplicate
any(bit_duplicated(x))  # full bit work, returns FALSE or TRUE
bit_anyDuplicated(x)    # early termination of bit work, returns 0 or position of first duplicate
# nolint end: any_duplicated_linter.