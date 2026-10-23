# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: fn_env.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 8

suppressPackageStartupMessages(library(rlang))
env <- child_env("base")
fn <- with_env(env, function() NULL)
identical(fn_env(fn), env)

other_env <- child_env("base")
fn_env(fn) <- other_env
identical(fn_env(fn), other_env)