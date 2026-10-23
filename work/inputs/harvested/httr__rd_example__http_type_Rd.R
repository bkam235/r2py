# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: http_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 8

suppressPackageStartupMessages(library(httr))
r1 <- GET("http://httpbin.org/image/png")
http_type(r1)
headers(r1)[["Content-Type"]]

r2 <- GET("http://httpbin.org/ip")
http_type(r2)
headers(r2)[["Content-Type"]]