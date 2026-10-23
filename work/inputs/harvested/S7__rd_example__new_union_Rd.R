# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: new_union.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 18

suppressPackageStartupMessages(library(S7))
logical_or_character <- new_union(class_logical, class_character)
logical_or_character
# or with shortcut syntax
logical_or_character <- class_logical | class_character

Foo <- new_class("Foo", properties = list(x = logical_or_character))
Foo(x = TRUE)
Foo(x = letters[1:5])
try(Foo(1:3))

bar <- new_generic("bar", "x")
# Use built-in union
method(bar, class_atomic) <- function(x) "Hi!"
bar
bar(TRUE)
bar(letters)
try(bar(NULL))