# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_dry_run.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 11

suppressPackageStartupMessages(library(httr2))
# httr2 adds default User-Agent, Accept, and Accept-Encoding headers
request("http://example.com") |> req_dry_run()

# the Authorization header is automatically redacted to avoid leaking
# credentials on the console
req <- request("http://example.com") |> req_auth_basic("user", "password")
req |> req_dry_run()

# if you need to see it, use redact_headers = FALSE
req |> req_dry_run(redact_headers = FALSE)