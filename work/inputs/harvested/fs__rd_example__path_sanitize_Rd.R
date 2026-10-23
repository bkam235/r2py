# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path_sanitize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 6

suppressPackageStartupMessages(library(fs))
# potentially unsafe string
str <- "~/.\u0001ssh/authorized_keys"
path_sanitize(str)

path_sanitize("..")