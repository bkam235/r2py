# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_oauth_password.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 11

suppressPackageStartupMessages(library(httr2))
req_auth <- function(req) {
  req_oauth_password(req,
    client = oauth_client("example", "https://example.com/get_token"),
    username = "username"
  )
}
if (interactive()) {
  request("https://example.com") |>
    req_auth()
}