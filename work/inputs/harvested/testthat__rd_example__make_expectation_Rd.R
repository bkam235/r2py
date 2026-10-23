# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: make_expectation.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 8

suppressPackageStartupMessages(library(testthat))
x <- 1:10
make_expectation(x)

make_expectation(mtcars$mpg)

df <- data.frame(x = 2)
make_expectation(df)