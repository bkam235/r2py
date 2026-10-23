# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: run-mold.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 8

suppressPackageStartupMessages(library(hardhat))
bp <- default_xy_blueprint()

outcomes <- mtcars["mpg"]
predictors <- mtcars
predictors$mpg <- NULL

run_mold(bp, x = predictors, y = outcomes)