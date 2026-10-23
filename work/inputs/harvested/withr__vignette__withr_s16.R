# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 11

suppressPackageStartupMessages(library(withr))
neatest <- function(x, sig_digits) {
  local_options(list(digits = sig_digits))
  print(x)
}

pi

neatest(pi, 2)

neatest(pi, 4)