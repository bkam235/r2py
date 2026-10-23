# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: clone.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 9

suppressPackageStartupMessages(library(bit))
x <- 1:12
  y <- x
  still.identical(x, y)
  y[1] <- y[1]
  still.identical(x, y)
  y <- clone(x)
  still.identical(x, y)
  rm(x, y); gc()