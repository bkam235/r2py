# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: locale-sensitive_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\locale-sensitive.R
# lines: 9

suppressPackageStartupMessages(library(stringr))
turkish_names <- c("İpek", "Işık", "İbrahim")
search_name <- "ipek"

# incorrect
str_equal(turkish_names, search_name, ignore_case = TRUE)

# correct
str_equal(turkish_names, search_name, ignore_case = TRUE, locale = "tr")