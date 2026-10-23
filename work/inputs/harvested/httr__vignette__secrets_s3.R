# r2py crawler metadata
# package: httr
# source_type: vignette
# topic: secrets_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\doc\secrets.R
# lines: 9

suppressPackageStartupMessages(library(httr))
my_secrets <- function() {
  path <- "~/secrets/secret.json"
  if (!file.exists(path)) {
    stop("Can't find secret file: '", path, "'")
  }
  
  jsonlite::read_json(path)
}