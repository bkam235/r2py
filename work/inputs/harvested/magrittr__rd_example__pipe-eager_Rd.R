# r2py crawler metadata
# package: magrittr
# source_type: rd_example
# topic: pipe-eager.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\help
# lines: 45

suppressPackageStartupMessages(library(magrittr))
f <- function(x) {
  message("foo")
  x
}
g <- function(x) {
  message("bar")
  x
}
h <- function(x) {
  message("baz")
  invisible(x)
}

# The following lazy pipe sequence is equivalent to `h(g(f()))`.
# Given R's lazy evaluation behaviour,`f()` and `g()` are lazily
# evaluated when `h()` is already running. This causes the messages
# to appear in reverse order:
NULL %>% f() %>% g() %>% h()

# Use the eager pipe to fix this:
NULL %!>% f() %!>% g() %!>% h()

# Or fix this by calling `force()` on the function arguments
f <- function(x) {
  force(x)
  message("foo")
  x
}
g <- function(x) {
  force(x)
  message("bar")
  x
}
h <- function(x) {
  force(x)
  message("baz")
  invisible(x)
}

# With strict functions, the arguments are evaluated sequentially
NULL %>% f() %>% g() %>% h()

# Instead of forcing, you can also check the type of your functions.
# Type-checking also has the effect of making your function lazy.