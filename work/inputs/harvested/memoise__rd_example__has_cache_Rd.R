# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: has_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 5

suppressPackageStartupMessages(library(memoise))
mem_sum <- memoise(sum)
has_cache(mem_sum)(1, 2, 3) # FALSE
mem_sum(1, 2, 3)
has_cache(mem_sum)(1, 2, 3) # TRUE