# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_collapse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 8

suppressPackageStartupMessages(library(cli))
ansi_collapse(letters)

# truncate
ansi_collapse(letters, trunc = 5)

# head style
ansi_collapse(letters, trunc = 5, style = "head")