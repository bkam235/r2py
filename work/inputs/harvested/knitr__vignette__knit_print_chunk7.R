# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_print_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_print.Rmd
# lines: 5

suppressPackageStartupMessages(library(knitr))
dummy_print = function(x, ...) {
  cat("I do not know what to print!")
  # this function implicitly returns an invisible NULL
}