# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: class_any.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 7

suppressPackageStartupMessages(library(S7))
foo <- new_generic("foo", "x")
method(foo, class_numeric) <- function(x) "number"
method(foo, class_any) <- function(x) "fallback"

foo(1)
foo("x")