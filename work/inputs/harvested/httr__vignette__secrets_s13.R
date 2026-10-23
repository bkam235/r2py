# r2py crawler metadata
# package: httr
# source_type: vignette
# topic: secrets_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\doc\secrets.R
# lines: 8

suppressPackageStartupMessages(library(httr))
my_secret <- function() {
  val <- Sys.getenv("SECRET")
  if (identical(val, "")) {
    stop("`SECRET` env var has not been set")
  }
  val
}