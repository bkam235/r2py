# r2py crawler metadata
# package: brio
# source_type: rd_example
# topic: readLines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brio\help
# lines: 11

suppressPackageStartupMessages(library(brio))
authors_file <- file.path(R.home("doc"), "AUTHORS")
data <- readLines(authors_file)

# Trying to use connections throws an error
con <- file(authors_file)
try(readLines(con))
close(con)

# Trying to use unsupported args throws a warning
data <- readLines(authors_file, encoding = "UTF-16")