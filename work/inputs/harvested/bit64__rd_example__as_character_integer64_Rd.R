# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: as.character.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 6

suppressPackageStartupMessages(library(bit64))
as.character(lim.integer64())
  as.bitstring(lim.integer64())
  as.bitstring(as.integer64(c(
   -2,-1,NA,0:2
  )))