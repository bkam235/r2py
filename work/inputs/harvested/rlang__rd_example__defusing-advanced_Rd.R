# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: defusing-advanced.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 37

suppressPackageStartupMessages(library(rlang))
# `exprs()` is the plural variant of `expr()`
exprs(foo, bar, bar)

# `quo()` and `quos()` are the quosure variants of `expr()` and `exprs()`
quo(foo)
quos(foo, bar)

# `enexpr()` and `enexprs()` are the naked variants of `enquo()` and `enquos()`
my_function1 <- function(arg) enexpr(arg)
my_function2 <- function(arg, ...) enexprs(arg, ...)
my_function1(1 + 1)
my_function2(1 + 1, 10 * 2)


# `ensym()` and `ensyms()` are symbol variants of `enexpr()` and `enexprs()`
my_function3 <- function(arg) ensym(arg)
my_function4 <- function(arg, ...) ensyms(arg, ...)

# The user must supply symbols
my_function3(foo)
my_function4(foo, bar)

# Complex expressions are an error
try(my_function3(1 + 1))
try(my_function4(1 + 1, 10 * 2))


# `enquo0()` and `enquos0()` disable injection operators
automatic_injection <- function(x) enquo(x)
no_injection <- function(x) enquo0(x)

automatic_injection(foo(!!!1:3))
no_injection(foo(!!!1:3))

# Injection can still be done explicitly
inject(no_injection(foo(!!!1:3)))