# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: return_from.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 15

suppressPackageStartupMessages(library(rlang))
fn <- function() {
  g(current_env())
  "ignored"
}
g <- function(env) {
  h(env)
  "ignored"
}
h <- function(env) {
  return_from(env, "early return")
  "ignored"
}

fn()