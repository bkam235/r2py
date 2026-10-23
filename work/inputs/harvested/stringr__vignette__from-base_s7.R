# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 11

suppressPackageStartupMessages(library(stringr))
hw <- "Hadley Wickham"

# base
substr(hw, start = 1, stop = 6)
substring(hw, first = 1) 

# stringr
str_sub(hw, start = 1, end = 6)
str_sub(hw, start = 1)
str_sub(hw, end = 6)