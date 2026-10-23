# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: rest_api.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 15

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
# a normal GET request
xfun::rest_api("https://mockhttp.org", "/get")
xfun::rest_api_raw("https://mockhttp.org", "/get")

# send the request with an auth header
xfun::rest_api("https://mockhttp.org", "/headers", "OPEN SESAME!")

# with query parameters
xfun::rest_api("https://mockhttp.org", "/response-headers", params = list(foo = "bar"))

# get the rate limit info from GitHub
xfun::github_api("/rate_limit")
}