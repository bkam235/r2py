# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: S7_inherits.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 13

suppressPackageStartupMessages(library(S7))
Foo1 <- new_class("Foo1")
Foo2 <- new_class("Foo2")

S7_inherits(Foo1(), Foo1)
check_is_S7(Foo1())
check_is_S7(Foo1(), Foo1)

S7_inherits(Foo1(), Foo2)
try(check_is_S7(Foo1(), Foo2))

if (getRversion() >= "4.3.0")
  inherits(Foo1(), Foo1)