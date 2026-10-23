# r2py crawler metadata
# package: withr
# source_type: vignette
# topic: withr_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\doc\withr.R
# lines: 9

suppressPackageStartupMessages(library(withr))
on_exit_stack <- function() {
  cat("put on socks\n")
  on.exit(cat("take off socks\n"), add = TRUE, after = FALSE)
  
  cat("put on shoes\n")
  on.exit(cat("take off shoes\n"), add = TRUE, after = FALSE)
}
on_exit_stack()