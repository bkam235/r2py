# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: is.sorted.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 9

suppressPackageStartupMessages(library(bit64))
x <- as.integer64(sample(c(rep(NA, 9), 1:9), 32, TRUE))
 length(x)
 na.count(x)
 nvalid(x)
 nunique(x)
 nties(x)
 table.integer64(x)
 x