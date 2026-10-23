# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: new_function.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 19

suppressPackageStartupMessages(library(rlang))
f <- function() letters
g <- new_function(NULL, quote(letters))
identical(f, g)

# Pass a list or pairlist of named arguments to create a function
# with parameters. The name becomes the parameter name and the
# argument the default value for this parameter:
new_function(list(x = 10), quote(x))
new_function(pairlist2(x = 10), quote(x))

# Use `exprs()` to create quoted defaults. Compare:
new_function(pairlist2(x = 5 + 5), quote(x))
new_function(exprs(x = 5 + 5), quote(x))

# Pass empty arguments to omit defaults. `list()` doesn't allow
# empty arguments but `pairlist2()` does:
new_function(pairlist2(x = , y = 5 + 5), quote(x + y))
new_function(exprs(x = , y = 5 + 5), quote(x + y))