# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: POST.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 19

suppressPackageStartupMessages(library(httr))
b2 <- "http://httpbin.org/post"
POST(b2, body = "A simple text string")
POST(b2, body = list(x = "A simple text string"))
POST(b2, body = list(y = upload_file(system.file("CITATION"))))
POST(b2, body = list(x = "A simple text string"), encode = "json")

# body can also be provided as a json string directly to deal
# with specific case, like an empty element in the json string.
# passing as string directly
POST(b2, body = '{"a":1,"b":{}}', encode = "raw")
# or building the json string before
json_body <- jsonlite::toJSON(list(a = 1, b = NULL), auto_unbox = TRUE)
POST(b2, body = json_body, encode = "raw")

# Various types of empty body:
POST(b2, body = NULL, verbose())
POST(b2, body = FALSE, verbose())
POST(b2, body = "", verbose())