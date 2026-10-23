# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: parse_vector.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 4

suppressPackageStartupMessages(library(readr))
x <- c("1", "2", "3", "NA")
parse_vector(x, col_integer())
parse_vector(x, col_double())