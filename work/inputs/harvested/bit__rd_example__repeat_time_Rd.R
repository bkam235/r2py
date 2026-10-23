# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: repeat.time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 5

suppressPackageStartupMessages(library(bit))
system.time(1 + 1)
  repeat.time(1 + 1)
  system.time(sort(runif(1e6)))
  repeat.time(sort(runif(1e6)))