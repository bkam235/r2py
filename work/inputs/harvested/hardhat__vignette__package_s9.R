# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 16

suppressPackageStartupMessages(library(hardhat))
simple_lm_bridge <- function(processed) {
  
  validate_outcomes_are_univariate(processed$outcomes)
  
  predictors <- as.matrix(processed$predictors)
  outcomes <- processed$outcomes[[1]]
  
  fit <- simple_lm_impl(predictors, outcomes)
  
  new_simple_lm(
    coefs = fit$coefs,
    coef_names = fit$coef_names,
    blueprint = processed$blueprint
  )
}