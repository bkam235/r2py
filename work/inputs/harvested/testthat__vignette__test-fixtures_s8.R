# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.R
# lines: 10

suppressPackageStartupMessages(library(testthat))
neat <- function(x, sig_digits) {
  op <- options(digits = sig_digits)
  on.exit(options(op), add = TRUE, after = FALSE)
  print(x)
}

pi
neat(pi, 2)
pi