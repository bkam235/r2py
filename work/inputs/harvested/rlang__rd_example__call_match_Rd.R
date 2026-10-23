# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: call_match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 6

suppressPackageStartupMessages(library(rlang))
# `call_match()` supports matching missing arguments to their
# defaults
fn <- function(x = "default") fn
call_match(quote(fn()), fn)
call_match(quote(fn()), fn, defaults = TRUE)