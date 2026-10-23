# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_has.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 7

suppressPackageStartupMessages(library(rlang))
parent <- child_env(NULL, foo = "foo")
env <- child_env(parent, bar = "bar")

# env does not own `foo` but sees it in its parent environment:
env_has(env, "foo")
env_has(env, "foo", inherit = TRUE)