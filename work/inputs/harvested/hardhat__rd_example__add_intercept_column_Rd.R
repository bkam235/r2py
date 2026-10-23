# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: add_intercept_column.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 6

suppressPackageStartupMessages(library(hardhat))
add_intercept_column(mtcars)

add_intercept_column(mtcars, "intercept")

add_intercept_column(as.matrix(mtcars))