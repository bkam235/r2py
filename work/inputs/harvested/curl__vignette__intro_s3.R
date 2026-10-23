# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 4

suppressPackageStartupMessages(library(curl))
tmp <- tempfile()
curl_download("https://hb.cran.dev/get?bar=456", tmp)
jsonlite::prettify(readLines(tmp))