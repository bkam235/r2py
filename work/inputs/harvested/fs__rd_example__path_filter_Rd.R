# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path_filter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 5

suppressPackageStartupMessages(library(fs))
path_filter(c("foo", "boo", "bar"), glob = "*oo")
path_filter(c("foo", "boo", "bar"), glob = "*oo", invert = TRUE)

path_filter(c("foo", "boo", "bar"), regexp = "b.r")