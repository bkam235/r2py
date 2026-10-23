# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: fct_encode_one_hot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 7

suppressPackageStartupMessages(library(hardhat))
fct_encode_one_hot(factor(letters))

fct_encode_one_hot(factor(letters[1:2], levels = letters))

set.seed(1234)
fct_encode_one_hot(factor(sample(letters[1:4], 10, TRUE)))