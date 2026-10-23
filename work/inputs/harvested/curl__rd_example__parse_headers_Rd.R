# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: parse_headers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 7

suppressPackageStartupMessages(library(curl))
req <- curl_fetch_memory("https://hb.cran.dev/redirect/3")
parse_headers(req$headers)
parse_headers(req$headers, multiple = TRUE)

# Parse into named list
parse_headers_list(req$headers)