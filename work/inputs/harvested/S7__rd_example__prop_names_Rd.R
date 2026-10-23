# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: prop_names.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 7

suppressPackageStartupMessages(library(S7))
Foo <- new_class("Foo", properties = list(a = class_character, b = class_integer))
f <- Foo()

prop_names(f)
prop_exists(f, "a")
prop_exists(f, "c")