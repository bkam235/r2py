# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: parse_media.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 5

suppressPackageStartupMessages(library(httr))
parse_media("text/plain")
parse_media("text/plain; charset=utf-8")
parse_media("text/plain; charset=\"utf-8\"")
parse_media("text/plain; randomparam=\";=;=\"")