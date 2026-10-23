# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: Extract.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 11

suppressPackageStartupMessages(library(bit))
x <- as.bit(c(FALSE, NA, TRUE))
  x[] <- c(FALSE, NA, TRUE)
  x[1:2]
  x[-3]
  x[ri(1, 2)]
  x[as.bitwhich(c(TRUE, TRUE, FALSE))]
  x[[1]]
  x[] <- TRUE
  x[1:2] <- FALSE
  x[[1]] <- TRUE