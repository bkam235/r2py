# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: col_strsplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 14

suppressPackageStartupMessages(library(crayon))
str <- red("I am red---") %+%
  green("and I am green-") %+%
  underline("I underlined")

cat(str, "\n")

# split at dashes, keep color
cat(col_strsplit(str, "[-]+")[[1]], sep = "\n")
strsplit(strip_style(str), "[-]+")

# split to characters, keep color
cat(col_strsplit(str, "")[[1]], "\n", sep = " ")
strsplit(strip_style(str), "")