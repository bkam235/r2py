# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: read_table.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 4

suppressPackageStartupMessages(library(readr))
ws <- readr_example("whitespace-sample.txt")
writeLines(read_lines(ws))
read_table(ws)