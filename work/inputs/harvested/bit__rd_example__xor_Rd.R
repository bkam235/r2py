# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: xor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 9

suppressPackageStartupMessages(library(bit))
x <- c(FALSE, FALSE, FALSE, NA, NA, NA, TRUE, TRUE, TRUE)
  y <- c(FALSE, NA, TRUE, FALSE, NA, TRUE, FALSE, NA, TRUE)

  x | y
  x | as.bit(y)
  x | as.bitwhich(y)
  x | as.which(y)
  x | ri(1, 1, 9)