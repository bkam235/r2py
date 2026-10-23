# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_environment.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 14

suppressPackageStartupMessages(library(rlang))
# Coerce a named vector to an environment:
env <- as_environment(mtcars)

# By default it gets the empty environment as parent:
identical(env_parent(env), empty_env())


# With strings it is a handy shortcut for pkg_env():
as_environment("base")
as_environment("rlang")

# With NULL it returns the empty environment:
as_environment(NULL)