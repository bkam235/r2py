# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: bit_rangediff.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 5

suppressPackageStartupMessages(library(bit))
bit_rangediff(c(1L, 6L), c(3L, 4L))
bit_rangediff(c(6L, 1L), c(3L, 4L))
bit_rangediff(c(6L, 1L), c(3L, 4L), revx=TRUE)
bit_rangediff(c(6L, 1L), c(3L, 4L), revx=TRUE, revy=TRUE)