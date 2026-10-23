# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_is_user_facing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 10

suppressPackageStartupMessages(library(rlang))
fn <- function() {
  env_is_user_facing(caller_env())
}

# Direct call of `fn()` from the global env
with(global_env(), fn())

# Indirect call of `fn()` from a package
with(ns_env("utils"), fn())