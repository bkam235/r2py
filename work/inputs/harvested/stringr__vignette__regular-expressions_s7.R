# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 9

suppressPackageStartupMessages(library(stringr))
# To create the regular expression, we need \\
dot <- "\\."

# But the expression itself only contains one:
writeLines(dot)

# And this tells R to look for an explicit .
str_extract(c("abc", "a.c", "bef"), "a\\.c")