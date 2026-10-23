# r2py crawler metadata
# package: digest
# source_type: rd_example
# topic: digest2int.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\digest\help
# lines: 4

suppressPackageStartupMessages(library(digest))
current <- digest2int("The quick brown fox jumps over the lazy dog", 0L)
target <- 1369346549L
stopifnot(identical(target, current))