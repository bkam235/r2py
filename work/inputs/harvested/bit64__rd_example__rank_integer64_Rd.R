# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: rank.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 6

suppressPackageStartupMessages(library(bit64))
x <- as.integer64(sample(c(rep(NA, 9), 1:9), 32, TRUE))
rank.integer64(x)

stopifnot(identical(rank.integer64(x),  rank(as.integer(x)
, na.last="keep", ties.method = "average")))