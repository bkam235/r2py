# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 25

suppressPackageStartupMessages(library(testthat))
expect_vector_length <- function(object, n) {  
  act <- quasi_label(rlang::enquo(object))

  # It's non-trivial to check if an object is a vector in base R so we
  # use an rlang helper
  if (!rlang::is_vector(act$val)) {
    fail(c(
      sprintf("Expected %s to be a vector", act$lab),
      sprintf("Actual type: %s", typeof(act$val))
    ))
  } else {
    act_n <- length(act$val)
    if (act_n != n) {
      fail(c(
        sprintf("Expected %s to have length %i.", act$lab, n),
        sprintf("Actual length: %i.", act_n)
      ))
    } else {
      pass()
    }
  }

  invisible(act$val)
}