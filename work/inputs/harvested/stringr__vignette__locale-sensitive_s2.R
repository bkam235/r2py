# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: locale-sensitive_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\locale-sensitive.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
# English
str_to_upper("i")
str_to_lower("I")

# Turkish
str_to_upper("i", locale = "tr")
str_to_lower("I", locale = "tr")