# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: cumsum.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 5

suppressPackageStartupMessages(library(bit64))
cumsum(rep(as.integer64(1), 12))
  diff(as.integer64(c(0,1:12)))
  cumsum(as.integer64(c(0, 1:12)))
  diff(cumsum(as.integer64(c(0,0,1:12))), differences=2)