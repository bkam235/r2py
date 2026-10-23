# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: length.bit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 83

suppressPackageStartupMessages(library(bit))
stopifnot(length(ri(1, 1, 32)) == 32)

  x <- as.bit(ri(32, 32, 32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 1)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 0)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 0)

  x <- as.bit(ri(1, 1, 32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 1)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 1)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 1)

  x <- as.bitwhich(bit(32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 0)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 0)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 0)

  x <- as.bitwhich(!bit(32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 32)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 16)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 32)

  x <- as.bitwhich(ri(32, 32, 32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 1)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 0)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 0)

  x <- as.bitwhich(ri(2, 32, 32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 31)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 15)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 31)

  x <- as.bitwhich(ri(1, 1, 32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 1)
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 1)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 1)

  x <- as.bitwhich(ri(1, 31, 32))
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 31)
  message("NOTE the change from 'some excluded' to 'all excluded' here")
  length(x) <- 16
  stopifnot(length(x) == 16)
  stopifnot(sum(x) == 16)
  length(x) <- 32
  stopifnot(length(x) == 32)
  stopifnot(sum(x) == 32)