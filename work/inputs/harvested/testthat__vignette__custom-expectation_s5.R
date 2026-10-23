# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 20

suppressPackageStartupMessages(library(testthat))
expect_length <- function(object, n) {  
  # 1. Capture object and label
  act <- quasi_label(rlang::enquo(object))
  
  act_n <- length(act$val)
  if (act_n != n) {
    # 2. Fail if expectations are violated
    fail(c(
      sprintf("Expected %s to have length %i.", act$lab, n),
      sprintf("Actual length: %i.", act_n)
    ))
  } else {
    # 3. Pass if expectations are met
    pass()
  }
  
  # 4. Invisibly return the input value
  invisible(act$val)
}