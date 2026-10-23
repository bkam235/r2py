# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: Discrete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 8

suppressPackageStartupMessages(library(e1071))
## a vector of length 30 whose elements are 1 with probability 0.2
## and 2 with probability 0.8.
rdiscrete (30, c(0.2, 0.8))

## a vector of length 100 whose elements are A, B, C, D.
## The probabilities of the four values have the relation 1:2:3:3
rdiscrete (100, c(1,2,3,3), c("A","B","C","D"))