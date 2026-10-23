# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: set_cookies.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 7

suppressPackageStartupMessages(library(httr))
set_cookies(a = 1, b = 2)
set_cookies(.cookies = c(a = "1", b = "2"))


GET("http://httpbin.org/cookies")
GET("http://httpbin.org/cookies", set_cookies(a = 1, b = 2))