# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: parse_expr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
# parse_expr() can parse any R expression:
parse_expr("mtcars %>% dplyr::mutate(cyl_prime = cyl / sd(cyl))")

# A string can contain several expressions separated by ; or \n
parse_exprs("NULL; list()\n foo(bar)")

# Use names to figure out which input produced an expression:
parse_exprs(c(foo = "1; 2", bar = "3"))

# You can also parse source files by passing a R connection. Let's
# create a file containing R code:
path <- tempfile("my-file.R")
cat("1; 2; mtcars", file = path)

# We can now parse it by supplying a connection:
parse_exprs(file(path))