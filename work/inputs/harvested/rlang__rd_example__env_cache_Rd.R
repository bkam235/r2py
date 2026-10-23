# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
e <- env(a = "foo")

# Returns existing binding
env_cache(e, "a", "default")

# Creates a `b` binding and returns its default value
env_cache(e, "b", "default")

# Now `b` is defined
e$b