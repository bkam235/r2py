# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_function.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 13

suppressPackageStartupMessages(library(rlang))
f <- as_function(~ .x + 1)
f(10)

g <- as_function(~ -1 * .)
g(4)

h <- as_function(~ .x - .y)
h(6, 3)

# Functions created from a formula have a special class:
is_lambda(f)
is_lambda(as_function(function() "foo"))