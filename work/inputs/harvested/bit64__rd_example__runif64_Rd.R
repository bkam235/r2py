# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: runif64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 11

suppressPackageStartupMessages(library(bit64))
runif64(12)
  runif64(12, -16, 16)
  runif64(12, 0, as.integer64(2^60)-1)  # not 2^60-1 !
  var(runif(1e4))
  var(as.double(runif64(1e4, 0, 2^40))/2^40)  # ~ = 1/12 = .08333

  table(sample(16, replace=FALSE))
  table(runif64(16, 1, 16, replace=FALSE))
  table(sample(16, replace=TRUE))
  table(runif64(16, 1, 16, replace=TRUE))