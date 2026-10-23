# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: all.equal.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 5

suppressPackageStartupMessages(library(bit64))
all.equal(as.integer64(1:10), as.integer64(0:9))
  all.equal(as.integer64(1:10), as.integer(1:10))
  all.equal(as.integer64(1:10), as.double(1:10))
  all.equal(as.integer64(1), as.double(1e300))