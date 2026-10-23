# r2py crawler metadata
# package: cpp11
# source_type: vignette
# topic: cpp11_s27
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\doc\cpp11.R
# lines: 8

suppressPackageStartupMessages(library(cpp11))
vacc2 <- function(age, female, ily) {
  p <- 0.25 + 0.3 * 1 / (1 - exp(0.04 * age)) + 0.1 * ily
  p <- p * ifelse(female, 1.25, 0.75)
  p <- pmax(0, p)
  p <- pmin(1, p)
  p
}