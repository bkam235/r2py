# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_strsplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 16

suppressPackageStartupMessages(library(cli))
str <- paste0(
  col_red("I am red---"),
  col_green("and I am green-"),
  style_underline("I underlined")
)

cat(str, "\n")

# split at dashes, keep color
cat(ansi_strsplit(str, "[-]+")[[1]], sep = "\n")
strsplit(ansi_strip(str), "[-]+")

# split to characters, keep color
cat(ansi_strsplit(str, "")[[1]], "\n", sep = " ")
strsplit(ansi_strip(str), "")