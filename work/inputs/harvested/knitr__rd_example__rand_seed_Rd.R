# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: rand_seed.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 4

suppressPackageStartupMessages(library(knitr))
eval(rand_seed)
rnorm(1)  # .Random.seed is created (or modified)
eval(rand_seed)