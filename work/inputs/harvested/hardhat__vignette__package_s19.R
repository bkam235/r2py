# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 12

suppressPackageStartupMessages(library(hardhat))
predict_simple_lm_bridge <- function(type, object, predictors) {
  
  type <- rlang::arg_match(type, "numeric")
  
  predictors <- as.matrix(predictors)
  
  switch(
    type,
    numeric = predict_simple_lm_numeric(object, predictors)
  )
}