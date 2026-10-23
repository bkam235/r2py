# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_chunk17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.Rmd
# lines: 9

suppressPackageStartupMessages(library(withr))
neat_with <- function(x, sig_digits) {
      # imagine lots of code here
      withr::with_options(
        list(digits = sig_digits),
        print(x)
      )
      # ... and a lot more code here
    }