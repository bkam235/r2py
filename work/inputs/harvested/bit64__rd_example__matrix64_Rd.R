# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: matrix64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 7

suppressPackageStartupMessages(library(bit64))
A = as.integer64(1:6)
dim(A) = 3:2

colSums(A)
rowSums(A)
aperm(A, 2:1)