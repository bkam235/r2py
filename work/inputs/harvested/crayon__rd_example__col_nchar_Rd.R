# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: col_nchar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 11

suppressPackageStartupMessages(library(crayon))
str <- paste(
  red("red"),
  "default",
  green("green")
)

cat(str, "\n")
nchar(str)
col_nchar(str)
nchar(strip_style(str))