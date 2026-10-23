# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_unbind.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 16

suppressPackageStartupMessages(library(rlang))
env <- env(foo = 1, bar = 2)
env_has(env, c("foo", "bar"))

# Remove bindings with `env_unbind()`
env_unbind(env, c("foo", "bar"))
env_has(env, c("foo", "bar"))

# With inherit = TRUE, it removes bindings in parent environments
# as well:
parent <- env(empty_env(), foo = 1, bar = 2)
env <- env(parent, foo = "b")

env_unbind(env, "foo", inherit = TRUE)
env_has(env, c("foo", "bar"))
env_has(env, c("foo", "bar"), inherit = TRUE)