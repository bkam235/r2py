# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_toupper.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 7

suppressPackageStartupMessages(library(cli))
ansi_toupper(col_red("Uppercase"))

ansi_tolower(col_red("LowerCase"))

x <- paste0(col_green("MiXeD"), col_red(" cAsE 123"))
ansi_chartr("iXs", "why", x)