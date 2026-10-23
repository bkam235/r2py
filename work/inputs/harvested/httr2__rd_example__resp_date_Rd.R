# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 8

suppressPackageStartupMessages(library(httr2))
resp <- response(headers = "Date: Wed, 01 Jan 2020 09:23:15 UTC")
resp |> resp_date()

# If server doesn't add header (unusual), you get the time the request
# was created:
resp <- response()
resp |> resp_date()