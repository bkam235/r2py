# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_which.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 9

suppressPackageStartupMessages(library(stringr))
fruit <- c("apple", "banana", "pear", "pineapple")
str_which(fruit, "a")

# Elements that don't match
str_which(fruit, "^p", negate = TRUE)

# Missings never match
str_which(c("a", NA, "b"), ".")