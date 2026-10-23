# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_oauth_refresh.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 4

suppressPackageStartupMessages(library(httr2))
client <- oauth_client("example", "https://example.com/get_token")
req <- request("https://example.com")
req |> req_oauth_refresh(client)