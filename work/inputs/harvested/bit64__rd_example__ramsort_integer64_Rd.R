# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: ramsort.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 22

suppressPackageStartupMessages(library(bit64))
x <- as.integer64(sample(c(rep(NA, 9), 1:9), 32, TRUE))
  x
  message("ramsort example")
  s <- clone(x)
  ramsort(s)
  message("s has been changed in-place - whether or not ramsort uses an in-place algorithm")
  s
  message("ramorder example")
  s <- clone(x)
  o <- seq_along(s)
  ramorder(s, o)
  message("o has been changed in-place - s remains unchanged")
  s
  o
  s[o]
  message("ramsortorder example")
  o <- seq_along(s)
  ramsortorder(s, o)
  message("s and o have both been changed in-place - this is much faster")
  s
  o