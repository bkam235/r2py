# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: authenticate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 6

suppressPackageStartupMessages(library(httr))
GET("http://httpbin.org/basic-auth/user/passwd")
GET(
  "http://httpbin.org/basic-auth/user/passwd",
  authenticate("user", "passwd")
)