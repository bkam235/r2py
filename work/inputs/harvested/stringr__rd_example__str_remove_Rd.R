# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_remove.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 4

suppressPackageStartupMessages(library(stringr))
fruits <- c("one apple", "two pears", "three bananas")
str_remove(fruits, "[aeiou]")
str_remove_all(fruits, "[aeiou]")