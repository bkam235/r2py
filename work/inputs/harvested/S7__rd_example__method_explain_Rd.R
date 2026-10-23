# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: method_explain.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 9

suppressPackageStartupMessages(library(S7))
Foo1 <- new_class("Foo1")
Foo2 <- new_class("Foo2", Foo1)

add <- new_generic("add", c("x", "y"))
method(add, list(Foo2, Foo1)) <- function(x, y) c(2, 1)
method(add, list(Foo1, Foo1)) <- function(x, y) c(1, 1)

method_explain(add, list(Foo2, Foo2))