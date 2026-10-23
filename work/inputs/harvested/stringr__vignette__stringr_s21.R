# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 5

suppressPackageStartupMessages(library(stringr))
a1 <- "\u00e1"
a2 <- "a\u0301"
c(a1, a2)
a1 == a2