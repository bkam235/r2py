# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: set_names.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 22

suppressPackageStartupMessages(library(rlang))
set_names(1:4, c("a", "b", "c", "d"))
set_names(1:4, letters[1:4])
set_names(1:4, "a", "b", "c", "d")

# If the second argument is omitted a vector is named with itself
set_names(letters[1:5])

# Alternatively you can supply a function
set_names(1:10, ~ letters[seq_along(.)])
set_names(head(mtcars), toupper)

# If the input vector is unnamed, it is first named after itself
# before the function is applied:
set_names(letters, toupper)

# `...` is passed to the function:
set_names(head(mtcars), paste0, "_foo")

# If length 1, the second argument is recycled to the length of the first:
set_names(1:3, "foo")
set_names(list(), "")