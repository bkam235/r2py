# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: resolution.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
resolution(1:10)
resolution((1:10) - 0.5)
resolution((1:10) - 0.5, FALSE)

# Note the difference between numeric and integer vectors
resolution(c(2, 10, 20, 50))
resolution(c(2L, 10L, 20L, 50L))