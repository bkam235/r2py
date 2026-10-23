# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 12

suppressPackageStartupMessages(library(hardhat))
try({
model <- simple_lm(bill_length_mm ~ body_mass_g + species, penguins)

# Pass in the data frame
predictors <- forge(penguins, model$blueprint)$predictors

predict_simple_lm_bridge("numeric", model, predictors)

# Partial matches are an error
predict_simple_lm_bridge("numer", model, predictors)
})