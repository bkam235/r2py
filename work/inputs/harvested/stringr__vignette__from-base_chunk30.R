# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_chunk30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.Rmd
# lines: 12

suppressPackageStartupMessages(library(stringr))
#| eval: !expr getRversion() >= "3.3.0"

fruit <- c("apple", "pear", "banana")

# base
strrep(fruit, 2)
strrep(fruit, 1:3)

# stringr
str_dup(fruit, 2)
str_dup(fruit, 1:3)