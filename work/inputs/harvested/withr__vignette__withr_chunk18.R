# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_chunk18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.Rmd
# lines: 6

suppressPackageStartupMessages(library(withr))
neat_local <- function(x, sig_digits) {
      withr::local_options(list(digits = sig_digits))
      print(x)
      # imagine lots of code here
    }