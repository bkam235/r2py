# r2py crawler metadata
# package: cachem
# source_type: rd_example
# topic: cache_layered.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cachem\help
# lines: 5

suppressPackageStartupMessages(library(cachem))
# Make a layered cache from a small memory cache and large disk cache
m <- cache_mem(max_size = 100 * 1024^2)
d <- cache_disk(max_size = 2 * 1024^3)
cl <- cache_layered(m, d)