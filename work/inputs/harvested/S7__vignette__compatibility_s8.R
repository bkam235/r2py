# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: compatibility_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\compatibility.R
# lines: 8

suppressPackageStartupMessages(library(S7))
Class1 <- new_class("Class1")
Class2 <- new_class("Class2")
Union1 <- new_union(Class1, Class2)

foo <- new_generic("foo", "x")
method(foo, Union1) <- function(x) ""
foo