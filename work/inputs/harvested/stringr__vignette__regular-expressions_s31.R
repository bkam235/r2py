# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 12

suppressPackageStartupMessages(library(stringr))
phone <- regex("
  \\(?       # optional opening parens
  (\\d{3})   # area code
  \\)?       # optional closing parens
  (?:-|\\ )? # optional dash or space
  (\\d{3})   # another three numbers
  (?:-|\\ )? # optional dash or space
  (\\d{3})   # three more numbers
  ", comments = TRUE)

str_match(c("514-791-8141", "(514) 791 8141"), phone)