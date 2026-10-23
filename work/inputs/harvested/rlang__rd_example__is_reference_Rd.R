# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_reference.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
# Reassigning an uncopyable object such as an environment creates a
# reference:
env <- env()
ref <- env
is_reference(ref, env)

# Due to copy-on-write optimisation, a copied vector can
# temporarily reference the original vector:
vec <- 1:10
copy <- vec
is_reference(copy, vec)

# Once you modify on of them, the copy is triggered in the
# background and the objects cease to reference each other:
vec[[1]] <- 100
is_reference(copy, vec)