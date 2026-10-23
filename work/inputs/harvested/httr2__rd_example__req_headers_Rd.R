# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_headers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 43

suppressPackageStartupMessages(library(httr2))
req <- request("http://example.com")

# Use req_headers() to add arbitrary additional headers to the request
req |>
  req_headers(MyHeader = "MyValue") |>
  req_dry_run()

# Repeated use overrides the previous value:
req |>
  req_headers(MyHeader = "Old value") |>
  req_headers(MyHeader = "New value") |>
  req_dry_run()

# Setting Accept to NULL uses curl's default:
req |>
  req_headers(Accept = NULL) |>
  req_dry_run()

# Setting it to "" removes it:
req |>
  req_headers(Accept = "") |>
  req_dry_run()

# If you need to repeat a header, provide a vector of values
# (this is rarely needed, but is important in a handful of cases)
req |>
  req_headers(HeaderName = c("Value 1", "Value 2", "Value 3")) |>
  req_dry_run()

# If you have headers in a list, use !!!
headers <- list(HeaderOne = "one", HeaderTwo = "two")
req |>
  req_headers(!!!headers, HeaderThree = "three") |>
  req_dry_run()

# Use `req_headers_redacted()`` to hide a header in the output
req_secret <- req |>
  req_headers_redacted(Secret = "this-is-private") |>
  req_headers(Public = "but-this-is-not")

req_secret
req_secret |> req_dry_run()