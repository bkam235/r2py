# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 11

suppressPackageStartupMessages(library(withr))
sloppy <- function(x, sig_digits) {
  options(digits = sig_digits)
  print(x)
}

pi

sloppy(pi, 2)

pi