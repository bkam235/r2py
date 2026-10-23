# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: new_quosure.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 32

suppressPackageStartupMessages(library(rlang))
# `new_quosure()` creates a quosure from its components. These are
# equivalent:
new_quosure(quote(foo), current_env())

quo(foo)

# `new_quosure()` always rewraps its input into a new quosure, even
# if the input is itself a quosure:
new_quosure(quo(foo))

# This is unlike `as_quosure()` which preserves its input if it's
# already a quosure:
as_quosure(quo(foo))


# `as_quosure()` uses the supplied environment with naked expressions:
env <- env(var = "thing")
as_quosure(quote(var), env)

# If the expression already carries an environment, this
# environment is preserved. This is the case for formulas and
# quosures:
as_quosure(~foo, env)

as_quosure(~foo)

# An environment must be supplied when the input is a naked
# expression:
try(
  as_quosure(quote(var))
)