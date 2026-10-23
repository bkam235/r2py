# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: fn_fmls.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 14

suppressPackageStartupMessages(library(rlang))
# Extract from current call:
fn <- function(a = 1, b = 2) fn_fmls()
fn()

# fn_fmls_syms() makes it easy to forward arguments:
call2("apply", !!! fn_fmls_syms(lapply))

# You can also change the formals:
fn_fmls(fn) <- list(A = 10, B = 20)
fn()

fn_fmls_names(fn) <- c("foo", "bar")
fn()