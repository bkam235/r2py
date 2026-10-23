# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: frev.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 7

suppressPackageStartupMessages(library(data.table))
# on vectors
x = setNames(1:10, letters[1:10])
frev(x)

# list
frev(list(1, "a", TRUE))