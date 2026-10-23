# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 9

suppressPackageStartupMessages(library(withr))
defer_stack <- function() {
  cat("put on socks\n")
  defer(cat("take off socks\n"))
  
  cat("put on shoes\n")
  defer(cat("take off shoes\n"))
}
defer_stack()