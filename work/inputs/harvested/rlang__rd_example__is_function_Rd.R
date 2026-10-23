# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_function.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 22

suppressPackageStartupMessages(library(rlang))
# Primitive functions are not closures:
is_closure(base::c)
is_primitive(base::c)

# On the other hand, internal functions are wrapped in a closure
# and appear as such from the R side:
is_closure(base::eval)

# Both closures and primitives are functions:
is_function(base::c)
is_function(base::eval)

# Many primitive functions evaluate arguments eagerly:
is_primitive_eager(base::c)
is_primitive_eager(base::list)
is_primitive_eager(base::`+`)

# However, primitives that operate on expressions, like quote() or
# substitute(), are lazy:
is_primitive_lazy(base::quote)
is_primitive_lazy(base::substitute)