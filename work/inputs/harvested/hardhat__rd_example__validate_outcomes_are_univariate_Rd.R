# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: validate_outcomes_are_univariate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 4

suppressPackageStartupMessages(library(hardhat))
validate_outcomes_are_univariate(data.frame(x = 1))

try(validate_outcomes_are_univariate(mtcars))