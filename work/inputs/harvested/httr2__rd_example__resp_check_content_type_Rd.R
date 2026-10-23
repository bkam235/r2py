# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_check_content_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 7

suppressPackageStartupMessages(library(httr2))
resp <- response(headers = list(`content-type` = "application/json"))
resp_check_content_type(resp, "application/json")
try(resp_check_content_type(resp, "application/xml"))

# `types` can also specify multiple valid types
resp_check_content_type(resp, c("application/xml", "application/json"))