# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s27
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 8

suppressPackageStartupMessages(library(bit))
# TODO(r-lib/lintr#773): nolint as a chunk option.
# nolint start: rep_len_linter.
b <- as.bit(c(FALSE, TRUE))
rev(b)
rep(b, 3)
rep(b, length.out=6)
# nolint end: rep_len_linter.