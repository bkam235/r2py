# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 9

suppressPackageStartupMessages(library(testthat))
sloppy <- function(x, sig_digits) {
  options(digits = sig_digits)
  print(x)
}

pi
sloppy(pi, 2)
pi