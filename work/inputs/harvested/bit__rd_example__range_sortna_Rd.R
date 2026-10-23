# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: range_sortna.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 7

suppressPackageStartupMessages(library(bit))
range_sortna(c(0L, 1L, NA, 2L))
range_sortna(c(2L, NA, 1L, 0L))
range_sortna(c(0L, 1L, NA, 2L), na.last=TRUE)
range_sortna(c(2L, NA, 1L, 0L), na.last=TRUE)
range_sortna(c(0L, 1L, NA, 2L), na.last=FALSE)
range_sortna(c(2L, NA, 1L, 0L), na.last=FALSE)