# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_user_agent.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 11

suppressPackageStartupMessages(library(httr2))
# Default user-agent:
request("http://example.com") |> req_dry_run()

request("http://example.com") |> req_user_agent("MyString") |> req_dry_run()

# If you're wrapping in an API in a package, it's polite to set the
# user agent to identify your package.
request("http://example.com") |>
  req_user_agent("MyPackage (http://mypackage.com)") |>
  req_dry_run()