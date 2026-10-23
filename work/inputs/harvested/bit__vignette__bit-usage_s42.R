# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s42
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 5

suppressPackageStartupMessages(library(bit))
x <- c(0L, NA, NA, 1L, 1L, 3L)
y <- c(NA, NA, 2L, 2L, 3L, 4L)
union(setdiff(x, y), setdiff(y, x))
bit_symdiff(x, y)