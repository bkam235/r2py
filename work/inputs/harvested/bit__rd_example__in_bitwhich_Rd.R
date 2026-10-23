# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: in.bitwhich.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 4

suppressPackageStartupMessages(library(bit))
x <- bitwhich(100)
x[3] <- TRUE
in.bitwhich(c(NA, 2, 3), x)