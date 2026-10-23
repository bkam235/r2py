# r2py crawler metadata
# package: httr2
# source_type: vignette
# topic: httr2_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\doc\httr2.R
# lines: 10

suppressPackageStartupMessages(library(httr2))
try({
request(example_url()) |>
  req_url_path("/status/404") |>
  req_perform()

request(example_url()) |>
  req_url_path("/status/500") |>
  req_perform()
})