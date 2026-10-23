# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: CoercionToStandard.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 18

suppressPackageStartupMessages(library(bit))
x <- ri(2, 5, 10)
  y <- as.logical(x)
  y
  stopifnot(identical(y, as.logical(as.bit(x))))
  stopifnot(identical(y, as.logical(as.bitwhich(x))))

  y <- as.integer(x)
  y
  stopifnot(identical(y, as.integer(as.logical(x))))
  stopifnot(identical(y, as.integer(as.bit(x))))
  stopifnot(identical(y, as.integer(as.bitwhich(x))))

  y <- as.double(x)
  y
  stopifnot(identical(y, as.double(as.logical(x))))
  stopifnot(identical(y, as.double(as.bit(x))))
  stopifnot(identical(y, as.double(as.bitwhich(x))))