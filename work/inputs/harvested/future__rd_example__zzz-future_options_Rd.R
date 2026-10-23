# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: zzz-future.options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 6

suppressPackageStartupMessages(library(future))
# Allow at most 5 MB globals per futures
options(future.globals.maxSize = 5e6)

# Be strict; catch all RNG mistakes
options(future.rng.onMisuse = "error")