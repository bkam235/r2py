# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 7

suppressPackageStartupMessages(library(withr))
neater <- function(x, sig_digits) {
  op <- options(digits = sig_digits) # record orig. "digits" & change "digits"
  defer(options(op))                 # schedule restoration of "digits"
  
  print(x)
}