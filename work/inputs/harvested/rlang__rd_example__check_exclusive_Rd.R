# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: check_exclusive.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 28

suppressPackageStartupMessages(library(rlang))
f <- function(x, y) {
  switch(
    check_exclusive(x, y),
    x = message("`x` was supplied."),
    y = message("`y` was supplied.")
  )
}

# Supplying zero or multiple arguments is forbidden
try(f())
try(f(NULL, NULL))

# The user must supply one of the mutually exclusive arguments
f(NULL)
f(y = NULL)


# With `.require` you can allow zero arguments
f <- function(x, y) {
  switch(
    check_exclusive(x, y, .require = FALSE),
    x = message("`x` was supplied."),
    y = message("`y` was supplied."),
    message("No arguments were supplied")
  )
}
f()