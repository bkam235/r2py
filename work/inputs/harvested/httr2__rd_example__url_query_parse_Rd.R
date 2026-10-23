# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: url_query_parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 5

suppressPackageStartupMessages(library(httr2))
str(url_query_parse("a=1&b=2"))

url_query_build(list(x = 1, y = "z"))
url_query_build(list(x = 1, y = 1:2), .multi = "explode")