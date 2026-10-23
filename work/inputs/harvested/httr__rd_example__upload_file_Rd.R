# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: upload_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 5

suppressPackageStartupMessages(library(httr))
citation <- upload_file(system.file("CITATION"))

POST("http://httpbin.org/post", body = citation)
POST("http://httpbin.org/post", body = list(y = citation))