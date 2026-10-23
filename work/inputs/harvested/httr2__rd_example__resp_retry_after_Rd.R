# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_retry_after.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 6

suppressPackageStartupMessages(library(httr2))
resp <- response(headers = "Retry-After: 30")
resp |> resp_retry_after()

resp <- response(headers = "Retry-After: Mon, 20 Sep 2025 21:44:05 UTC")
resp |> resp_retry_after()