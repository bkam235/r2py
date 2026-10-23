# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_auth_basic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 13

suppressPackageStartupMessages(library(httr2))
req <- request("http://example.com") |> req_auth_basic("hadley", "SECRET")
req
req |> req_dry_run()

# httr2 does its best to redact the Authorization header so that you don't
# accidentally reveal confidential data. Use `redact_headers` to reveal it:
print(req, redact_headers = FALSE)
req |> req_dry_run(redact_headers = FALSE)

# We do this because the authorization header is not encrypted and the
# so password can easily be discovered:
rawToChar(jsonlite::base64_dec("aGFkbGV5OlNFQ1JFVA=="))