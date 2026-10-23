# r2py crawler metadata
# package: jsonlite
# source_type: rd_example
# topic: read_json.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\help
# lines: 9

suppressPackageStartupMessages(library(jsonlite))
tmp <- tempfile()
write_json(iris, tmp)

# Nested lists
read_json(tmp)

# A data frame
read_json(tmp, simplifyVector = TRUE)