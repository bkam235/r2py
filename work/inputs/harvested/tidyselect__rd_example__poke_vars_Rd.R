# r2py crawler metadata
# package: tidyselect
# source_type: rd_example
# topic: poke_vars.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\help
# lines: 41

suppressPackageStartupMessages(library(tidyselect))
poke_vars(letters)
peek_vars()

# Now that the variables are registered, the helpers can figure out
# the locations of elements within the variable vector:
all_of(c("d", "z"))

# In a function be sure to restore the previous variables. An exit
# hook is the best way to do it:
fn <- function(vars) {
  old <- poke_vars(vars)
  on.exit(poke_vars(old))

  all_of("d")
}
fn(letters)
fn(letters[3:5])

# The previous variables are still registered after fn() was
# called:
peek_vars()


# It is recommended to use the scoped variant as it restores the
# state automatically when the function returns:
fn <- function(vars) {
  scoped_vars(vars)
  starts_with("r")
}
fn(c("red", "blue", "rose"))

# The with_vars() helper makes it easy to pass an expression that
# should be evaluated in a variable context. Thanks to lazy
# evaluation, you can just pass the expression argument from your
# wrapper to with_vars():
fn <- function(expr) {
  vars <- c("red", "blue", "rose")
  with_vars(vars, expr)
}
fn(starts_with("r"))