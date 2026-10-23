# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: keypos.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 5

suppressPackageStartupMessages(library(bit64))
x <- as.integer64(sample(c(rep(NA, 9), 1:9), 32, TRUE))
keypos(x)

stopifnot(identical(keypos(x),  match.integer64(x, sort(unique(x), na.last=FALSE))))