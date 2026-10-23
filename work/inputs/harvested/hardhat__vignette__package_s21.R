# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 12

suppressPackageStartupMessages(library(hardhat))
predict.simple_lm <- function(object, new_data, type = "numeric", ...) {
  
  # Enforces column order, type, column names, etc
  processed <- forge(new_data, object$blueprint)
  
  out <- predict_simple_lm_bridge(type, object, processed$predictors)
  
  validate_prediction_size(out, new_data)
  
  out
}