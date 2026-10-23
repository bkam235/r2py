# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_parent.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 19

suppressPackageStartupMessages(library(rlang))
# Get the parent environment with env_parent():
env_parent(global_env())

# Or the tail environment with env_tail():
env_tail(global_env())

# By default, env_parent() returns the parent environment of the
# current evaluation frame. If called at top-level (the global
# frame), the following two expressions are equivalent:
env_parent()
env_parent(base_env())

# This default is more handy when called within a function. In this
# case, the enclosure environment of the function is returned
# (since it is the parent of the evaluation frame):
enclos_env <- env()
fn <- set_env(function() env_parent(), enclos_env)
identical(enclos_env, fn())