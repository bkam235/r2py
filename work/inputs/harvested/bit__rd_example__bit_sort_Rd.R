# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: bit_sort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 9

suppressPackageStartupMessages(library(bit))
bit_sort(c(2L, 1L, NA, NA, 1L, 2L))
bit_sort(c(2L, 1L, NA, NA, 1L, 2L), na.last=FALSE)
bit_sort(c(2L, 1L, NA, NA, 1L, 2L), na.last=TRUE)


x <- sample(1e7, replace=TRUE)
system.time(bit_sort(x))
system.time(sort(x))