# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: forge_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\forge.R
# lines: 6

suppressPackageStartupMessages(library(hardhat))
try({
test_missing_column <- subset(penguin_test, select = -species)

forge(test_missing_column, formula_eng)
})