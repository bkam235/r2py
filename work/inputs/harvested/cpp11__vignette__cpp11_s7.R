# r2py crawler metadata
# package: cpp11
# source_type: vignette
# topic: cpp11_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\doc\cpp11.R
# lines: 8

suppressPackageStartupMessages(library(cpp11))
sum_r <- function(x) {
  total <- 0
  for (i in seq_along(x)) {
    total <- total + x[i]
  }
  total
}