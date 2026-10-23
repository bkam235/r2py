# r2py crawler metadata
# package: jsonlite
# source_type: rd_example
# topic: unbox.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\help
# lines: 12

suppressPackageStartupMessages(library(jsonlite))
toJSON(list(foo=123))
toJSON(list(foo=unbox(123)))

# Auto unbox vectors of length one:
x = list(x=1:3, y = 4, z = "foo", k = NULL)
toJSON(x)
toJSON(x, auto_unbox = TRUE)

x <- iris[1,]
toJSON(list(rec=x))
toJSON(list(rec=unbox(x)))