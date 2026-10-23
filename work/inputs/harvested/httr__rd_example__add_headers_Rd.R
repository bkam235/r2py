# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: add_headers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 15

suppressPackageStartupMessages(library(httr))
add_headers(a = 1, b = 2)
add_headers(.headers = c(a = "1", b = "2"))


GET("http://httpbin.org/headers")

# Add arbitrary headers
GET(
  "http://httpbin.org/headers",
  add_headers(version = version$version.string)
)

# Override default headers with empty strings
GET("http://httpbin.org/headers", add_headers(Accept = ""))