# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: inject.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
# inject() simply evaluates its argument with injection
# support. These expressions are equivalent:
2 * 3
inject(2 * 3)
inject(!!2 * !!3)

# Injection with `!!` can be useful to insert objects or
# expressions within other expressions, like formulas:
lhs <- sym("foo")
rhs <- sym("bar")
inject(!!lhs ~ !!rhs + 10)

# Injection with `!!!` splices lists of arguments in function
# calls:
args <- list(na.rm = TRUE, finite = 0.2)
inject(mean(1:10, !!!args))