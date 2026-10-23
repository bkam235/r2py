# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 6

suppressPackageStartupMessages(library(stringr))
# base
grep(pattern = "g", x = fruit, value = TRUE)

# stringr
str_subset(fruit, pattern = "g")