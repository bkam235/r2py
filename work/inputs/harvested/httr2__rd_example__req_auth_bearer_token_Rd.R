# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_auth_bearer_token.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 7

suppressPackageStartupMessages(library(httr2))
req <- request("http://example.com") |> req_auth_bearer_token("sdaljsdf093lkfs")
req

# httr2 does its best to redact the Authorization header so that you don't
# accidentally reveal confidential data. Use `redact_headers` to reveal it:
print(req, redact_headers = FALSE)