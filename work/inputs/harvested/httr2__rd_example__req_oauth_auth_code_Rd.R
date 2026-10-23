# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_oauth_auth_code.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 11

suppressPackageStartupMessages(library(httr2))
req_auth_github <- function(req) {
  req_oauth_auth_code(
    req,
    client = example_github_client(),
    auth_url = "https://github.com/login/oauth/authorize"
  )
}

request("https://api.github.com/user") |>
  req_auth_github()