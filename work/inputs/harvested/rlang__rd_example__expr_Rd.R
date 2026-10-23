# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: expr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 23

suppressPackageStartupMessages(library(rlang))
# R normally returns the result of an expression
1 + 1

# `expr()` defuses the expression that you have supplied and
# returns it instead of its value
expr(1 + 1)

expr(toupper(letters))

# It supports _injection_ with `!!` and `!!!`. This is a convenient
# way of modifying part of an expression by injecting other
# objects.
var <- "cyl"
expr(with(mtcars, mean(!!sym(var))))

vars <- c("cyl", "am")
expr(with(mtcars, c(!!!syms(vars))))

# Compare to the normal way of building expressions
call("with", call("mean", sym(var)))

call("with", call2("c", !!!syms(vars)))