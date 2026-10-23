# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
fruit <- c("apple", "banana", "pear", "pineapple")

# base
grepl(pattern = "a", x = fruit)

# stringr
str_detect(fruit, pattern = "a")