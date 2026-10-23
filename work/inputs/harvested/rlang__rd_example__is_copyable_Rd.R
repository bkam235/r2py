# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_copyable.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 10

suppressPackageStartupMessages(library(rlang))
# Let's add attributes with structure() to uncopyable types. Since
# they are not copied, the attributes are changed in place:
env <- env()
structure(env, foo = "bar")
env

# These objects that can only be changed with side effect are not
# copyable:
is_copyable(env)