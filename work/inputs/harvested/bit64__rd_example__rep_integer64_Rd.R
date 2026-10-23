# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: rep.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 4

suppressPackageStartupMessages(library(bit64))
rep(as.integer64(1:2), 6)
  rep(as.integer64(1:2), c(6,6))
  rep(as.integer64(1:2), length.out=6)