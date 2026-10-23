# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: expr_label.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 18

suppressPackageStartupMessages(library(rlang))
# To labellise a function argument, first capture it with
# substitute():
fn <- function(x) expr_label(substitute(x))
fn(x:y)

# Strings are encoded
expr_label("a\nb")

# Names and expressions are quoted with ``
expr_label(quote(x))
expr_label(quote(a + b + c))

# Long expressions are collapsed
expr_label(quote(foo({
  1 + 2
  print(x)
})))