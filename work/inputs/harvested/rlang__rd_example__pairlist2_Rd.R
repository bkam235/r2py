# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: pairlist2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 8

suppressPackageStartupMessages(library(rlang))
# Unlike `exprs()`, `pairlist2()` evaluates its arguments.
new_function(pairlist2(x = 1, y = 3 * 6), quote(x * y))
new_function(exprs(x = 1, y = 3 * 6), quote(x * y))

# It preserves missing arguments, which is useful for creating
# parameters without defaults:
new_function(pairlist2(x = , y = 3 * 6), quote(x * y))