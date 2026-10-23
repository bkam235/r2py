# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
bananas <- c("banana", "Banana", "BANANA")
str_detect(bananas, "banana")
str_detect(bananas, regex("banana", ignore_case = TRUE))