# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: encoding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 6

suppressPackageStartupMessages(library(readr))
guess_encoding(readr_example("mtcars.csv"))
guess_encoding(read_lines_raw(readr_example("mtcars.csv")))
guess_encoding(read_file_raw(readr_example("mtcars.csv")))

guess_encoding("a\n\u00b5\u00b5")