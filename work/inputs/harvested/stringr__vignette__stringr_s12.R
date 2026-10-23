# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 7

suppressPackageStartupMessages(library(stringr))
x <- c("y", "i", "k")
str_order(x)

str_sort(x)
# In Lithuanian, y comes between i and k
str_sort(x, locale = "lt")