# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: parse_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 5

suppressPackageStartupMessages(library(curl))
# Parse dates in many formats
parse_date("Sunday, 06-Nov-94 08:49:37 GMT")
parse_date("06 Nov 1994 08:49:37")
parse_date("20040911 +0200")