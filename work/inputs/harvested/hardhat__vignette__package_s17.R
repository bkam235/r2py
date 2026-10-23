# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 11

suppressPackageStartupMessages(library(hardhat))
predict_simple_lm_numeric <- function(object, predictors) {
  
  coefs <- object$coefs
  
  pred <- as.vector(predictors %*% coefs)
  
  out <- spruce_numeric(pred)
  
  out
}