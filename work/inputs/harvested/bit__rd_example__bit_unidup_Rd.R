# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: bit_unidup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 16

suppressPackageStartupMessages(library(bit))
bit_unique(c(2L, 1L, NA, NA, 1L, 2L))
bit_unique(c(2L, 1L, NA, NA, 1L, 2L), na.rm=FALSE)
bit_unique(c(2L, 1L, NA, NA, 1L, 2L), na.rm=TRUE)

bit_duplicated(c(2L, 1L, NA, NA, 1L, 2L))
bit_duplicated(c(2L, 1L, NA, NA, 1L, 2L), na.rm=FALSE)
bit_duplicated(c(2L, 1L, NA, NA, 1L, 2L), na.rm=TRUE)

bit_anyDuplicated(c(2L, 1L, NA, NA, 1L, 2L))
bit_anyDuplicated(c(2L, 1L, NA, NA, 1L, 2L), na.rm=FALSE)
bit_anyDuplicated(c(2L, 1L, NA, NA, 1L, 2L), na.rm=TRUE)

bit_sumDuplicated(c(2L, 1L, NA, NA, 1L, 2L))
bit_sumDuplicated(c(2L, 1L, NA, NA, 1L, 2L), na.rm=FALSE)
bit_sumDuplicated(c(2L, 1L, NA, NA, 1L, 2L), na.rm=TRUE)