# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: fn_body.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 8

suppressPackageStartupMessages(library(rlang))
# fn_body() is like body() but always returns a block:
fn <- function() do()
body(fn)
fn_body(fn)

# It also throws an error when used on a primitive function:
try(fn_body(base::list))