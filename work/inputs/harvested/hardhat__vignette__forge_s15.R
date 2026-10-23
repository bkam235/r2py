# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: forge_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\forge.R
# lines: 6

suppressPackageStartupMessages(library(hardhat))
try({
penguin_test_no_outcome <- subset(penguin_test, select = -bill_length_mm)

forge(penguin_test_no_outcome, recipe_eng_log_outcome)
})