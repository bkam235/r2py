# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_headers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 12

suppressPackageStartupMessages(library(httr2))
resp <- request("https://httr2.r-lib.org") |> req_perform()
resp |> resp_headers()
resp |> resp_headers("x-")

resp |> resp_header_exists("server")
resp |> resp_header("server")
# Headers are case insensitive
resp |> resp_header("SERVER")

# Returns NULL if header doesn't exist
resp |> resp_header("this-header-doesnt-exist")