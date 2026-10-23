# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: bit_sort_unique.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 15

suppressPackageStartupMessages(library(bit))
bit_sort_unique(c(2L, 1L, NA, NA, 1L, 2L))
bit_sort_unique(c(2L, 1L, NA, NA, 1L, 2L), na.last=FALSE)
bit_sort_unique(c(2L, 1L, NA, NA, 1L, 2L), na.last=TRUE)
bit_sort_unique(c(2L, 1L, NA, NA, 1L, 2L), decreasing = TRUE)
bit_sort_unique(c(2L, 1L, NA, NA, 1L, 2L), decreasing = TRUE, na.last=FALSE)
bit_sort_unique(c(2L, 1L, NA, NA, 1L, 2L), decreasing = TRUE, na.last=TRUE)


x <- sample(1e7, replace=TRUE)
system.time(bit_sort_unique(x))
system.time(sort(unique(x)))
x <- sample(1e7)
system.time(bit_sort_unique(x))
system.time(sort(x))