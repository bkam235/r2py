# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 6

suppressPackageStartupMessages(library(curl))
req <- curl_fetch_memory("https://api.github.com/users/ropensci")
req$times

req2 <- curl_fetch_memory("https://api.github.com/users/rstudio")
req2$times