# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: breaks_exp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 5

suppressPackageStartupMessages(library(scales))
# Small range
demo_continuous(c(100, 102), transform = "exp", breaks = breaks_exp())
# Large range
demo_continuous(c(0, 100), transform = "exp", breaks = breaks_exp(n = 4))