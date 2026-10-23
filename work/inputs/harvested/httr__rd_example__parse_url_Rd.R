# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: parse_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 9

suppressPackageStartupMessages(library(httr))
parse_url("http://google.com/")
parse_url("http://google.com:80/")
parse_url("http://google.com:80/?a=1&b=2")

url <- parse_url("http://google.com/")
url$scheme <- "https"
url$query <- list(q = "hello")
build_url(url)