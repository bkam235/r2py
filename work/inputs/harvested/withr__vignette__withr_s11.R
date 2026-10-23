# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 9

suppressPackageStartupMessages(library(withr))
defer_queue <- function() {
  cat("Adam gets in line for ice cream\n")
  defer(cat("Adam gets ice cream\n"), priority = "last")

  cat("Beth gets in line for ice cream\n")
  defer(cat("Beth gets ice cream\n"), priority = "last")
}
defer_queue()