# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_clone.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 28

suppressPackageStartupMessages(library(rlang))
# A clone initially contains the same bindings as the original
# environment
env <- env(a = 1, b = 2)
clone <- env_clone(env)

env_print(clone)
env_print(env)

# But it can acquire new bindings or change existing ones without
# impacting the original environment
env_bind(clone, a = "foo", c = 3)

env_print(clone)
env_print(env)


# `env_coalesce()` copies bindings from one environment to another
lhs <- env(a = 1)
rhs <- env(a = "a", b = "b", c = "c")
env_coalesce(lhs, rhs)
env_print(lhs)

# To copy all the bindings from `rhs` into `lhs`, first delete the
# conflicting bindings from `rhs`
env_unbind(lhs, env_names(rhs))
env_coalesce(lhs, rhs)
env_print(lhs)