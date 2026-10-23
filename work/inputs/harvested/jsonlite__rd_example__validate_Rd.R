# r2py crawler metadata
# package: jsonlite
# source_type: rd_example
# topic: validate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\help
# lines: 8

suppressPackageStartupMessages(library(jsonlite))
#Output from toJSON and serializeJSON should pass validation
myjson <- toJSON(mtcars)
validate(myjson) #TRUE

#Something bad happened
truncated <- substring(myjson, 1, 100)
validate(truncated) #FALSE