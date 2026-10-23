# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 22

suppressPackageStartupMessages(library(hardhat))
new_simple_lm <- function(coefs, coef_names, blueprint) {
  
  if (!is.numeric(coefs)) {
    stop("`coefs` should be a numeric vector.", call. = FALSE)
  }
  
  if (!is.character(coef_names)) {
    stop("`coef_names` should be a character vector.", call. = FALSE)
  }
  
  if (length(coefs) != length(coef_names)) {
    stop("`coefs` and `coef_names` must have the same length.")
  }
  
  new_model(
    coefs = coefs, 
    coef_names = coef_names,
    blueprint = blueprint, 
    class = "simple_lm"
  )
}