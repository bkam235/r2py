# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: drop_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 9

suppressPackageStartupMessages(library(memoise))
mem_sum <- memoise(sum)
mem_sum(1, 2, 3)
mem_sum(2, 3, 4)
has_cache(mem_sum)(1, 2, 3) # TRUE
has_cache(mem_sum)(2, 3, 4) # TRUE
drop_cache(mem_sum)(1, 2, 3) # TRUE
has_cache(mem_sum)(1, 2, 3) # FALSE
has_cache(mem_sum)(2, 3, 4) # TRUE