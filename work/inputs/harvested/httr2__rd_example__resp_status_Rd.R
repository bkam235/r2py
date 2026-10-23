# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_status.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 6

suppressPackageStartupMessages(library(httr2))
# An HTTP status code you're unlikely to see in the wild:
resp <- response(418)
resp |> resp_is_error()
resp |> resp_status()
resp |> resp_status_desc()