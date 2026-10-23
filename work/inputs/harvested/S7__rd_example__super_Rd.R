# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: super.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 36

suppressPackageStartupMessages(library(S7))
Foo1 <- new_class("Foo1", properties = list(x = class_numeric, y = class_numeric))
Foo2 <- new_class("Foo2", Foo1, properties = list(z = class_numeric))

total <- new_generic("total", "x")
method(total, Foo1) <- function(x) x@x + x@y

# This won't work because it'll be stuck in an infinite loop:
method(total, Foo2) <- function(x) total(x) + x@z

# We could write
method(total, Foo2) <- function(x) x@x + x@y + x@z
# but then we'd need to remember to update it if the implementation
# for total(<Foo1>) ever changed.

# So instead we use `super()` to call the method for the parent class:
method(total, Foo2) <- function(x) total(super(x, to = Foo1)) + x@z
total(Foo2(1, 2, 3))

# To see the difference between convert() and super() we need a
# method that calls another generic

bar1 <- new_generic("bar1", "x")
method(bar1, Foo1) <- function(x) 1
method(bar1, Foo2) <- function(x) 2

bar2 <- new_generic("bar2", "x")
method(bar2, Foo1) <- function(x) c(1, bar1(x))
method(bar2, Foo2) <- function(x) c(2, bar1(x))

obj <- Foo2(1, 2, 3)
bar2(obj)
# convert() affects every generic:
bar2(convert(obj, to = Foo1))
# super() only affects the _next_ call to a generic:
bar2(super(obj, to = Foo1))