# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: countsort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 4

suppressPackageStartupMessages(library(bit))
countsort(c(2L, 0L, 1L, NA, 2L))
countsort(c(2L, 0L, 1L, NA, 2L), na.last=TRUE)
countsort(c(2L, 0L, 1L, NA, 2L), na.last=FALSE)