# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_seed.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 10

suppressPackageStartupMessages(library(withr))
# Same random values:
with_preserve_seed(runif(5))
with_preserve_seed(runif(5))

# Use a pseudorandom value as seed to advance the RNG and pick a different
# value for the next call:
with_seed(seed <- sample.int(.Machine$integer.max, 1L), runif(5))
with_seed(seed, runif(5))
with_seed(seed <- sample.int(.Machine$integer.max, 1L), runif(5))