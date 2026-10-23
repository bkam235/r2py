# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_get_headers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 7

suppressPackageStartupMessages(library(httr2))
req <- request("http://example.com")
req <- req_headers(req, a = 1L, b = 2L, .redact = "a")

req_get_headers(req, "drop")
req_get_headers(req, "redact")
req_get_headers(req, "reveal")