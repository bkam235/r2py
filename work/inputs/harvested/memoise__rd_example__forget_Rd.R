# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: forget.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 7

suppressPackageStartupMessages(library(memoise))
memX <- memoise(function() { Sys.sleep(1); runif(1) })
# The forget() function
system.time(print(memX()))
system.time(print(memX()))
forget(memX)
system.time(print(memX()))