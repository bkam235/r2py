# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 13

suppressPackageStartupMessages(library(stringr))
shopping_list <- c("apples x4", "bag of flour", "10", "milk x2")

# base
matches <- regexpr(pattern = "\\d+", text = shopping_list) # digits
regmatches(shopping_list, m = matches)

matches <- gregexpr(pattern = "[a-z]+", text = shopping_list) # words
regmatches(shopping_list, m = matches)

# stringr
str_extract(shopping_list, pattern = "\\d+") 
str_extract_all(shopping_list, "[a-z]+")