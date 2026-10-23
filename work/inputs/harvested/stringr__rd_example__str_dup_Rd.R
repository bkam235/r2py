# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_dup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 6

suppressPackageStartupMessages(library(stringr))
fruit <- c("apple", "pear", "banana")
str_dup(fruit, 2)
str_dup(fruit, 2, sep = " ")
str_dup(fruit, 1:3)
str_c("ba", str_dup("na", 0:5))