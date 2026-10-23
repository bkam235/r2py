# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_content_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 9

suppressPackageStartupMessages(library(httr2))
resp <- response(headers = "Content-type: text/html; charset=utf-8")
resp |> resp_content_type()
resp |> resp_encoding()

# No Content-Type header
resp <- response()
resp |> resp_content_type()
resp |> resp_encoding()