# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: sass_file_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 6

suppressPackageStartupMessages(library(sass))
# Create a cache with the default settings
cache <- sass_file_cache(sass_cache_context_dir())

# Clear the cache
cache$reset()