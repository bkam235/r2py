# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: http_error.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 13

suppressPackageStartupMessages(library(httr))
# You can pass a url:
http_error("http://www.google.com")
http_error("http://httpbin.org/status/404")

# Or a request
r <- GET("http://httpbin.org/status/201")
http_error(r)


# Or an (integer) status code
http_error(200L)
http_error(404L)