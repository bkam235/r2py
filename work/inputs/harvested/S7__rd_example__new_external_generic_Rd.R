# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: new_external_generic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 5

suppressPackageStartupMessages(library(S7))
MyClass <- new_class("MyClass")

your_generic <- new_external_generic("stats", "median", "x")
method(your_generic, MyClass) <- function(x) "Hi!"