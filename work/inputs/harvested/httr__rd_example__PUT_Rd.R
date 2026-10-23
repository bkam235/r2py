# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: PUT.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 9

suppressPackageStartupMessages(library(httr))
POST("http://httpbin.org/put")
PUT("http://httpbin.org/put")

b2 <- "http://httpbin.org/put"
PUT(b2, body = "A simple text string")
PUT(b2, body = list(x = "A simple text string"))
PUT(b2, body = list(y = upload_file(system.file("CITATION"))))
PUT(b2, body = list(x = "A simple text string"), encode = "json")