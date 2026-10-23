# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: validate_predictors_are_numeric.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 9

suppressPackageStartupMessages(library(hardhat))
# All good
check_predictors_are_numeric(mtcars)

# Species is not numeric
check_predictors_are_numeric(iris)

# This gives an intelligent error message
try(validate_predictors_are_numeric(iris))