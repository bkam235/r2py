# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: as.which.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 8

suppressPackageStartupMessages(library(bit))
r <- ri(5, 20, 100)
  x <- as.which(r)
  x

  stopifnot(identical(x, as.which(as.logical(r))))
  stopifnot(identical(x, as.which(as.bitwhich(r))))
  stopifnot(identical(x, as.which(as.bit(r))))