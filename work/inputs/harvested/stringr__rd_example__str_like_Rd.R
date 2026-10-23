# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_like.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 13

suppressPackageStartupMessages(library(stringr))
fruit <- c("apple", "banana", "pear", "pineapple")
str_like(fruit, "app")
str_like(fruit, "app%")
str_like(fruit, "APP%")
str_like(fruit, "ba_ana")
str_like(fruit, "%apple")

str_ilike(fruit, "app")
str_ilike(fruit, "app%")
str_ilike(fruit, "APP%")
str_ilike(fruit, "ba_ana")
str_ilike(fruit, "%apple")