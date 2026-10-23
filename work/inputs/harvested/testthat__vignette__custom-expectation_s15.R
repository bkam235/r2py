# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 19

suppressPackageStartupMessages(library(testthat))
expect_length_ <- function(act, n, trace_env = caller_env()) {
  act_n <- length(act$val)
  if (act_n != n) {
    fail(
      sprintf("%s has length %i, not length %i.", act$lab, act_n, n), 
      trace_env = trace_env
    )
  } else {
    pass()
  }
}

expect_length <- function(object, n) {  
  act <- quasi_label(rlang::enquo(object))

  expect_length_(act, n)
  invisible(act$val)
}