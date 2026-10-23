# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: new_S3_class.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 8

suppressPackageStartupMessages(library(S7))
# No checking, just used for dispatch
Date <- new_S3_class("Date")

my_generic <- new_generic("my_generic", "x")
method(my_generic, Date) <- function(x) "This is a date"

my_generic(Sys.Date())