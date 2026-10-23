# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: recompose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 9

suppressPackageStartupMessages(library(hardhat))
df <- vctrs::data_frame(x = 1)

recompose(df)
recompose(df, composition = "matrix")

# All columns must be numeric to convert to a matrix
df <- vctrs::data_frame(x = 1, y = "a")
try(recompose(df, composition = "matrix"))