# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s48
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 5

suppressPackageStartupMessages(library(bit))
x <- c(NA, NA, 1L, 1L, 2L, 3L)
sum(duplicated(x))      # full hash work, returns FALSE or TRUE
sum(bit_duplicated(x))  # full bit work, returns FALSE or TRUE
bit_sumDuplicated(x)    # early termination of bit work, returns 0 or position of first duplicated