# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: partial.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 44

suppressPackageStartupMessages(library(purrr))
# Partial is designed to replace the use of anonymous functions for
# filling in function arguments. Instead of:
compact1 <- function(x) discard(x, is.null)

# we can write:
compact2 <- partial(discard, .p = is.null)

# partial() works fine with functions that do non-standard
# evaluation
my_long_variable <- 1:10
plot2 <- partial(plot, my_long_variable)
plot2()
plot2(runif(10), type = "l")

# Note that you currently can't partialise arguments multiple times:
my_mean <- partial(mean, na.rm = TRUE)
my_mean <- partial(my_mean, na.rm = FALSE)
try(my_mean(1:10))


# The evaluation of arguments normally occurs "lazily". Concretely,
# this means that arguments are repeatedly evaluated across invocations:
f <- partial(runif, n = rpois(1, 5))
f
f()
f()

# You can unquote an argument to fix it to a particular value.
# Unquoted arguments are evaluated only once when the function is created:
f <- partial(runif, n = !!rpois(1, 5))
f
f()
f()


# By default, partialised arguments are passed before new ones:
my_list <- partial(list, 1, 2)
my_list("foo")

# Control the position of these arguments by passing an empty
# `... = ` argument:
my_list <- partial(list, 1, ... = , 2)
my_list("foo")