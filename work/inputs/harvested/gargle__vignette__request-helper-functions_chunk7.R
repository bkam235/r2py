# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: request-helper-functions_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\request-helper-functions.Rmd
# lines: 6

suppressPackageStartupMessages(library(gargle))
#| eval: false
# googledrive::
request_make <- function(x, ...) {
  gargle::request_make(x, ..., user_agent = drive_ua())
}