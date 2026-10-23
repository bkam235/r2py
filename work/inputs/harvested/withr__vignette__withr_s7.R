# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 12

suppressPackageStartupMessages(library(withr))
neater <- function(x, sig_digits) {
  op <- options(digits = sig_digits)
  defer(options(op))
  print(x)
}

pi

neater(pi, 2)

pi