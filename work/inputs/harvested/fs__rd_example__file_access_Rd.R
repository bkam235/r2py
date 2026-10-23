# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: file_access.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 6

suppressPackageStartupMessages(library(fs))
file_access("/")
file_access("/", "read")
file_access("/", "write")

file_exists("WOMBATS")