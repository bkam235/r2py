# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
x <- c("abcdef", "ghifjk")

# The 3rd letter
str_sub(x, 3, 3)

# The 2nd to 2nd-to-last character
str_sub(x, 2, -2)