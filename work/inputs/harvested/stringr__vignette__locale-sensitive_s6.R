# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: locale-sensitive_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\locale-sensitive.R
# lines: 11

suppressPackageStartupMessages(library(stringr))
czech_words <- c("had", "chata", "hrad", "chůze")
lithuanian_words <- c("ąžuolas", "ėglė", "šuo", "yra", "žuvis")

# incorrect
str_sort(czech_words)
str_sort(lithuanian_words)

# correct
str_sort(czech_words, locale = "cs")
str_sort(lithuanian_words, locale = "lt")