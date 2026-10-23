# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 14

suppressPackageStartupMessages(library(hardhat))
simple_lm_impl <- function(predictors, outcomes) {
  lm_fit <- lm.fit(predictors, outcomes)
  
  coefs <- lm_fit$coefficients
  
  coef_names <- names(coefs)
  coefs <- unname(coefs)
  
  list(
    coefs = coefs,
    coef_names = coef_names
  )
}