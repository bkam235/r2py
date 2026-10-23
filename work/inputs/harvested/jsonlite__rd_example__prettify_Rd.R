# r2py crawler metadata
# package: jsonlite
# source_type: rd_example
# topic: prettify.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\help
# lines: 5

suppressPackageStartupMessages(library(jsonlite))
myjson <- toJSON(cars)
cat(myjson)
prettify(myjson)
minify(myjson)