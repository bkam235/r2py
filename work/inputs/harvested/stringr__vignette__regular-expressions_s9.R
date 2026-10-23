# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 6

suppressPackageStartupMessages(library(stringr))
x <- c("a.b.c.d", "aeb")
starts_with <- "a.b"

str_detect(x, paste0("^", starts_with))
str_detect(x, paste0("^\\Q", starts_with, "\\E"))