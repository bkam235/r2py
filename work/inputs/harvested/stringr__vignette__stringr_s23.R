# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 6

suppressPackageStartupMessages(library(stringr))
i <- c("I", "İ", "i", "ı")
i

str_subset(i, coll("i", ignore_case = TRUE))
str_subset(i, coll("i", ignore_case = TRUE, locale = "tr"))