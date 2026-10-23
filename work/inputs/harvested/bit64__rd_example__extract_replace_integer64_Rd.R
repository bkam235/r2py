# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: extract.replace.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 7

suppressPackageStartupMessages(library(bit64))
as.integer64(1:12)[1:3]
  x <- as.integer64(1:12)
  dim(x) <- c(3,4)
  x
  x[]
  x[,2:3]