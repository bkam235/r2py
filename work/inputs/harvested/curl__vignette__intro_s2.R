# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 5

suppressPackageStartupMessages(library(curl))
req <- curl_fetch_memory("https://hb.cran.dev/get?foo=123")
str(req)
parse_headers(req$headers)
jsonlite::prettify(rawToChar(req$content))