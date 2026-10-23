# r2py crawler metadata
# package: httr
# source_type: vignette
# topic: secrets_chunk15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\doc\secrets.Rmd
# lines: 6

suppressPackageStartupMessages(library(httr))
skip_if_no_auth <- function() {
  if (identical(Sys.getenv("MY_SECRET"), "")) {
    skip("No authentication available")
  }
}