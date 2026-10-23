# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_nchar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 11

suppressPackageStartupMessages(library(cli))
str <- paste(
  col_red("red"),
  "default",
  col_green("green")
)

cat(str, "\n")
nchar(str)
ansi_nchar(str)
nchar(ansi_strip(str))