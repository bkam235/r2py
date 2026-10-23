# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 9

suppressPackageStartupMessages(library(withr))
on_exit_last_one_wins <- function() {
  cat("put on socks\n")
  on.exit(cat("take off socks\n"))
  
  cat("put on shoes\n")
  on.exit(cat("take off shoes\n"))
}
on_exit_last_one_wins()