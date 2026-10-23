# r2py crawler metadata
# package: cpp11
# source_type: vignette
# topic: cpp11_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\doc\cpp11.R
# lines: 9

suppressPackageStartupMessages(library(cpp11))
vacc1 <- function(age, female, ily) {
  n <- length(age)
  out <- numeric(n)
  for (i in seq_len(n)) {
    out[i] <- vacc1a(age[i], female[i], ily[i])
  }
  out
}