# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 10

suppressPackageStartupMessages(library(stringr))
fruits <- c("apple", "banana", "pear", "pineapple")

# base
sub("[aeiou]", "-", fruits)
gsub("[aeiou]", "-", fruits)

# stringr
str_replace(fruits, "[aeiou]", "-")
str_replace_all(fruits, "[aeiou]", "-")