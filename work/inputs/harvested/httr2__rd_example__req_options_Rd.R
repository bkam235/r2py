# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 8

suppressPackageStartupMessages(library(httr2))
# req_options() allows you to access curl options that are not otherwise
# exposed by httr2. For example, in very special cases you may need to
# turn off SSL verification. This is generally a bad idea so httr2 doesn't
# provide a convenient wrapper, but if you really know what you're doing
# you can still access this libcurl option:
req <- request("https://example.com") |>
  req_options(ssl_verifypeer = 0)