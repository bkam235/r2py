# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: frequency_weights.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 7

suppressPackageStartupMessages(library(hardhat))
# Record that the first observation has 10 replicates, the second has 12
# replicates, and so on
frequency_weights(c(10, 12, 2, 1))

# Fractional values are not allowed
try(frequency_weights(c(1.5, 2.3, 10)))