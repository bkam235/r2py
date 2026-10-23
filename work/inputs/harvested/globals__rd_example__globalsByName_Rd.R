# r2py crawler metadata
# package: globals
# source_type: rd_example
# topic: globalsByName.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\globals\help
# lines: 38

suppressPackageStartupMessages(library(globals))
f <- function(x = 42, ...) {
  globalsByName("x")
}

globals <- f()
str(globals)

globals <- f(3.14)
str(globals)


g <- function(x = 42, ...) {
  globalsByName("...")
}

globals <- g()
str(globals)

globals <- g(3.14)
str(globals)

globals <- g(3.14, 1L, b = 2L, c = 3L)
str(globals)


h <- function(x = 42, ...) {
  globalsByName("..2")
}

globals <- h(x = 3.14, a = 1, b = 2)
str(globals)

globals <- g(3.14)
str(globals)

globals <- g(3.14, 1L, b = 2L, c = 3L)
str(globals)