# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: modify_in.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 21

suppressPackageStartupMessages(library(purrr))
# Recall that pluck() returns a component of a data structure that
# might be arbitrarily deep
x <- list(list(bar = 1, foo = 2))
pluck(x, 1, "foo")

# Use assign_in() to modify the pluck location:
str(assign_in(x, list(1, "foo"), 100))
# Or zap to remove it
str(assign_in(x, list(1, "foo"), zap()))

# Like pluck(), this works even when the element (or its parents) don't exist
pluck(x, 1, "baz")
str(assign_in(x, list(2, "baz"), 100))

# modify_in() applies a function to that location and update the
# element in place:
modify_in(x, list(1, "foo"), \(x) x * 200)

# Additional arguments are passed to the function in the ordinary way:
modify_in(x, list(1, "foo"), `+`, 100)