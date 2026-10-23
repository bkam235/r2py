# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_link_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 10

suppressPackageStartupMessages(library(httr2))
# Simulate response from GitHub code search
resp <- response(headers = paste0("Link: ",
  '<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=2>; rel="next",',
  '<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=34>; rel="last"'
))

resp_link_url(resp, "next")
resp_link_url(resp, "last")
resp_link_url(resp, "prev")