# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: response.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 4

suppressPackageStartupMessages(library(httr2))
response()
response(404, method = "POST")
response(headers = c("Content-Type: text/html", "Content-Length: 300"))