# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: regular_minor_breaks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
m <- extended_breaks()(c(1, 10))
regular_minor_breaks()(m, c(1, 10), n = 2)

n <- extended_breaks()(c(0, -9))
regular_minor_breaks(reverse = TRUE)(n, c(0, -9), n = 2)