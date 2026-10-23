# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 12

suppressPackageStartupMessages(library(withr))
neat <- function(x, sig_digits) {
  op <- options(digits = sig_digits)
  on.exit(options(op), add = TRUE)
  print(x)
}

pi

neat(pi, 2)

pi