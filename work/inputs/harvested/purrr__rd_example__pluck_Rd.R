# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: pluck.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 52

suppressPackageStartupMessages(library(purrr))
# Let's create a list of data structures:
obj1 <- list("a", list(1, elt = "foo"))
obj2 <- list("b", list(2, elt = "bar"))
x <- list(obj1, obj2)

# pluck() provides a way of retrieving objects from such data
# structures using a combination of numeric positions, vector or
# list names, and accessor functions.

# Numeric positions index into the list by position, just like `[[`:
pluck(x, 1)
# same as x[[1]]

# Index from the back
pluck(x, -1)
# same as x[[2]]

pluck(x, 1, 2)
# same as x[[1]][[2]]

# Supply names to index into named vectors:
pluck(x, 1, 2, "elt")
# same as x[[1]][[2]][["elt"]]

# By default, pluck() consistently returns `NULL` when an element
# does not exist:
pluck(x, 10)
try(x[[10]])

# You can also supply a default value for non-existing elements:
pluck(x, 10, .default = NA)

# The map() functions use pluck() by default to retrieve multiple
# values from a list:
map_chr(x, 1)
map_int(x, c(2, 1))

# pluck() also supports accessor functions:
my_element <- function(x) x[[2]]$elt
pluck(x, 1, my_element)
pluck(x, 2, my_element)

# Even for this simple data structure, this is more readable than
# the alternative form because it requires you to read both from
# right-to-left and from left-to-right in different parts of the
# expression:
my_element(x[[1]])

# If you have a list of accessors, you can splice those in with `!!!`:
idx <- list(1, my_element)
pluck(x, !!!idx)