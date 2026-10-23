# r2py crawler metadata
# package: brio
# source_type: rd_example
# topic: read_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brio\help
# lines: 5

suppressPackageStartupMessages(library(brio))
authors_file <- file.path(R.home("doc"), "AUTHORS")
data <- read_file(authors_file)
data_raw <- read_file_raw(authors_file)
identical(data, rawToChar(data_raw))