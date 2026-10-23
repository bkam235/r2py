# r2py crawler metadata
# package: purrr
# source_type: vignette
# topic: purrr_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\doc\purrr.R
# lines: 6

suppressPackageStartupMessages(library(purrr))
x <- 1:3

triple <- function(x) x * 3
out <- map(x, triple)
str(out)