# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_bury.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 14

suppressPackageStartupMessages(library(rlang))
orig_env <- env(a = 10)
fn <- set_env(function() a, orig_env)

# fn() currently sees `a` as the value `10`:
fn()

# env_bury() will bury the current scope of fn() behind a new
# environment:
fn <- env_bury(fn, a = 1000)
fn()

# Even though the symbol `a` is still defined deeper in the scope:
orig_env$a