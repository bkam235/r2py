# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: nested_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\nested.R
# lines: 6

suppressPackageStartupMessages(library(foreach))
sim <- function(a, b) {
  x <- 10 * a + b
  err <- abs(a - b)
  list(x=x, err=err)
}