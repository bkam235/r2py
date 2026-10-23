# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: identical.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 4

suppressPackageStartupMessages(library(bit64))
i64 <- as.double(NA); class(i64) <- "integer64"
  identical(i64-1, i64+1)
  identical.integer64(i64-1, i64+1)