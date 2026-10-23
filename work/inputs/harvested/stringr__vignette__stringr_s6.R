# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
x <- c("abc", "defghi")
str_pad(x, 10) # default pads on left
str_pad(x, 10, "both")