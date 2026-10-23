# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: locale-sensitive_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\locale-sensitive.R
# lines: 7

suppressPackageStartupMessages(library(stringr))
dutch_sentence <- "ijsland is een prachtig land in Noord-Europa."

# Incorrect
str_to_sentence(dutch_sentence)
# Correct
str_to_sentence(dutch_sentence, locale = "nl")