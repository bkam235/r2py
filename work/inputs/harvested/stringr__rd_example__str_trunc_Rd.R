# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_trunc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 7

suppressPackageStartupMessages(library(stringr))
x <- "This string is moderately long"
rbind(
  str_trunc(x, 20, "right"),
  str_trunc(x, 20, "left"),
  str_trunc(x, 20, "center")
)