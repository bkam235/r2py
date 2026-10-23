# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: validate_outcomes_are_factors.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 6

suppressPackageStartupMessages(library(hardhat))
# Not a factor column.
check_outcomes_are_factors(data.frame(x = 1))

# All good
check_outcomes_are_factors(data.frame(x = factor(c("A", "B"))))