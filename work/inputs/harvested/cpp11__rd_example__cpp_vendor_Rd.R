# r2py crawler metadata
# package: cpp11
# source_type: rd_example
# topic: cpp_vendor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\help
# lines: 12

suppressPackageStartupMessages(library(cpp11))
# create a new directory
dir <- tempfile()
dir.create(dir)

# vendor the cpp11 headers into the directory
cpp_vendor(dir)

list.files(file.path(dir, "inst", "include", "cpp11"))

# cleanup
unlink(dir, recursive = TRUE)