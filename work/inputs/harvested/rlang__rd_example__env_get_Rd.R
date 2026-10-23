# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_get.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 12

suppressPackageStartupMessages(library(rlang))
parent <- child_env(NULL, foo = "foo")
env <- child_env(parent, bar = "bar")

# This throws an error because `foo` is not directly defined in env:
# env_get(env, "foo")

# However `foo` can be fetched in the parent environment:
env_get(env, "foo", inherit = TRUE)

# You can also avoid an error by supplying a default value:
env_get(env, "foo", default = "FOO")