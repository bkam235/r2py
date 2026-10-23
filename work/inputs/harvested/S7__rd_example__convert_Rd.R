# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: convert.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 33

suppressPackageStartupMessages(library(S7))
Foo1 <- new_class("Foo1", properties = list(x = class_integer))
Foo2 <- new_class("Foo2", Foo1, properties = list(y = class_double))

# Downcasting: S7 provides a default implementation for coercing an object
# to one of its parent classes:
convert(Foo2(x = 1L, y = 2), to = Foo1)

# Upcasting: S7 also provides a default implementation for coercing an object
# to one of its child classes:
convert(Foo1(x = 1L), to = Foo2)
convert(Foo1(x = 1L), to = Foo2, y = 2.5)  # Set new property
convert(Foo1(x = 1L), to = Foo2, x = 2L, y = 2.5)  # Override existing and set new

# For all other cases, you'll need to provide your own.
try(convert(Foo1(x = 1L), to = class_integer))

method(convert, list(Foo1, class_integer)) <- function(from, to) {
  from@x
}
convert(Foo1(x = 1L), to = class_integer)

# Note that conversion does not respect inheritance so if we define a
# convert method for integer to foo1
method(convert, list(class_integer, Foo1)) <- function(from, to) {
  Foo1(x = from)
}
convert(1L, to = Foo1)

# Converting to Foo2 will still error
try(convert(1L, to = Foo2))
# This is probably not surprising because foo2 also needs some value
# for `@y`, but it definitely makes dispatch for convert() special