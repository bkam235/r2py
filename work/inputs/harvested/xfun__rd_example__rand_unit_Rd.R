# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: rand_unit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
rand_unit(10)
rand_unit(10, seed = 0)
rand_unit(10, seed = 0)  # identical results
rand_unit(10, seed = Sys.getpid())