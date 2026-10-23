# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: is.memoised.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 4

suppressPackageStartupMessages(library(memoise))
mem_lm <- memoise(lm)
is.memoised(lm) # FALSE
is.memoised(mem_lm) # TRUE