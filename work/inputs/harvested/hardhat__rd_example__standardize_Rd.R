# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: standardize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 11

suppressPackageStartupMessages(library(hardhat))
standardize(1:5)

standardize(factor(letters[1:5]))

mat <- matrix(1:10, ncol = 2)
colnames(mat) <- c("a", "b")
standardize(mat)

df <- data.frame(x = 1:5, y = 6:10)
standardize(df)