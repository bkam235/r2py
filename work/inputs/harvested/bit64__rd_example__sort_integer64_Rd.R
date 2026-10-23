# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: sort.integer64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 9

suppressPackageStartupMessages(library(bit64))
x <- as.integer64(sample(c(rep(NA, 9), 1:9), 32, TRUE))
  x
  sort(x)
  message("the following has default optimize='time' which is faster but requires more RAM
, this calls 'ramorder'")
  order.integer64(x)
  message("slower with less RAM, this calls 'ramsortorder'")
  order.integer64(x, optimize="memory")