# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 4

suppressPackageStartupMessages(library(fs))
path("foo", "bar", "baz", ext = "zip")

path("foo", letters[1:3], ext = "txt")