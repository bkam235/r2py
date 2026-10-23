# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: timeout.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 4

suppressPackageStartupMessages(library(memoise))
a <- function(n) { runif(n) }
memA <- memoise(a, ~timeout(10))
memA(2)