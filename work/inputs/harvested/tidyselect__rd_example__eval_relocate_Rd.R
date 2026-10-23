# r2py crawler metadata
# package: tidyselect
# source_type: rd_example
# topic: eval_relocate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\help
# lines: 34

suppressPackageStartupMessages(library(tidyselect))
library(rlang)

# Interpret defused code as a request to relocate
x <- expr(c(mpg, disp))
after <- expr(wt)
eval_relocate(x, mtcars, after = after)

# Supplying neither `before` nor `after` will move the selection to the
# left-hand side
eval_relocate(x, mtcars)

# Within a function, use `enquo()` to defuse a single argument.
# Note that `before` and `after` must also be defused with `enquo()`.
my_relocator <- function(x, expr, before = NULL, after = NULL) {
  eval_relocate(enquo(expr), x, before = enquo(before), after = enquo(after))
}

my_relocator(mtcars, vs, before = hp)

# Here is an example of using `eval_relocate()` to implement `relocate()`.
# Note that the dots are passed on as a defused call to `c(...)`.
relocate <- function(.x, ..., .before = NULL, .after = NULL) {
  pos <- eval_relocate(
    expr(c(...)),
    .x,
    before = enquo(.before),
    after = enquo(.after)
  )
  set_names(.x[pos], names(pos))
}

relocate(mtcars, vs, .before = hp)
relocate(mtcars, starts_with("d"), .after = last_col())