# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: run-forge.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 10

suppressPackageStartupMessages(library(hardhat))
bp <- default_xy_blueprint()

outcomes <- mtcars["mpg"]
predictors <- mtcars
predictors$mpg <- NULL

mold <- run_mold(bp, x = predictors, y = outcomes)

run_forge(mold$blueprint, new_data = predictors)