# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: content_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 10

suppressPackageStartupMessages(library(httr))
GET("http://httpbin.org/headers")

GET("http://httpbin.org/headers", accept_json())
GET("http://httpbin.org/headers", accept("text/csv"))
GET("http://httpbin.org/headers", accept(".doc"))

GET("http://httpbin.org/headers", content_type_xml())
GET("http://httpbin.org/headers", content_type("text/csv"))
GET("http://httpbin.org/headers", content_type(".xml"))