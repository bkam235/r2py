# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 10

suppressPackageStartupMessages(library(stringr))
fruits <- c(
  "apples and oranges and pears and bananas",
  "pineapples and mangos and guavas"
)
# base
strsplit(fruits, " and ")

# stringr
str_split(fruits, " and ")