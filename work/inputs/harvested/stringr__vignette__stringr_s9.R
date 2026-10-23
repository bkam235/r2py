# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
x <- c("  a   ", "b   ",  "   c")
str_trim(x)
str_trim(x, "left")