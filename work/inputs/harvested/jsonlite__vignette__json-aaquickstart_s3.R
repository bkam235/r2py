# r2py crawler metadata
# package: jsonlite
# source_type: vignette
# topic: json-aaquickstart_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\doc\json-aaquickstart.R
# lines: 6

suppressPackageStartupMessages(library(jsonlite))
# A JSON array of primitives
json <- '["Mario", "Peach", null, "Bowser"]'

# Simplifies into an atomic vector
fromJSON(json)