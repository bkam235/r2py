# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: mold_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\mold.R
# lines: 11

suppressPackageStartupMessages(library(hardhat))
k_cols <- mold(~ species, penguins)

k_minus_one_cols <- mold(
  ~ species, penguins, 
  blueprint = default_formula_blueprint(intercept = TRUE)
)

colnames(k_cols$predictors)

colnames(k_minus_one_cols$predictors)