# r2py crawler metadata
# package: jsonlite
# source_type: rd_example
# topic: gzjson.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\help
# lines: 4

suppressPackageStartupMessages(library(jsonlite))
str <- as_gzjson_b64(iris[1:5,])
cat(str)
parse_gzjson_b64(str)