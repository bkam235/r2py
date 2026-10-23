# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: parse_http_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 6

suppressPackageStartupMessages(library(httr))
parse_http_date("Sun, 06 Nov 1994 08:49:37 GMT")
parse_http_date("Sunday, 06-Nov-94 08:49:37 GMT")
parse_http_date("Sun Nov  6 08:49:37 1994")

http_date(Sys.time())