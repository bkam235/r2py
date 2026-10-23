# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 9

suppressPackageStartupMessages(library(stringr))
fruit3 <- c("papaya", "lime", "apple")

# base
str(gregexpr(pattern = "p", text = fruit3))

# stringr
str_locate(fruit3, pattern = "p")
str_locate_all(fruit3, pattern = "p")