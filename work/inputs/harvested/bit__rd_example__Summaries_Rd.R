# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: Summaries.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 18

suppressPackageStartupMessages(library(bit))
l <- c(NA, FALSE, TRUE)
  b <- as.bit(l)

  all(l)
  all(b)
  all(b, range=c(3, 3))
  all.booltype(l, range=c(3, 3))

  min(l)
  min(b)

  sum(l)
  sum(b)

  summary(l)
  summary(b)
  summary.booltype(l)