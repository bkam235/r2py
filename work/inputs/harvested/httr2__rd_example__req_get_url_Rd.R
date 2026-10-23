# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_get_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 5

suppressPackageStartupMessages(library(httr2))
request("https://httpbin.org") |>
  req_url_path("/get") |>
  req_url_query(hello = "world") |>
  req_get_url()