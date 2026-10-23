# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: enquo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 26

suppressPackageStartupMessages(library(rlang))
# `enquo()` defuses the expression supplied by your user
f <- function(arg) {
  enquo(arg)
}

f(1 + 1)

# `enquos()` works with arguments and dots. It returns a list of
# expressions
f <- function(...) {
  enquos(...)
}

f(1 + 1, 2 * 10)


# `enquo()` and `enquos()` enable _injection_ and _embracing_ for
# your users
g <- function(arg) {
  f({{ arg }} * 2)
}
g(100)

column <- sym("cyl")
g(!!column)