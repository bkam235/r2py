# r2py crawler metadata
# package: cpp11
# source_type: vignette
# topic: cpp11_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\doc\cpp11.R
# lines: 8

suppressPackageStartupMessages(library(cpp11))
vacc1a <- function(age, female, ily) {
  p <- 0.25 + 0.3 * 1 / (1 - exp(0.04 * age)) + 0.1 * ily
  p <- p * if (female) 1.25 else 0.75
  p <- max(0, p)
  p <- min(1, p)
  p
}