# r2py crawler metadata
# package: jsonlite
# source_type: rd_example
# topic: base64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\help
# lines: 4

suppressPackageStartupMessages(library(jsonlite))
str <- base64_enc(serialize(iris, NULL))
out <- unserialize(base64_dec(str))
stopifnot(identical(out, iris))