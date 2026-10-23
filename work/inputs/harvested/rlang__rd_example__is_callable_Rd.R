# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_callable.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 19

suppressPackageStartupMessages(library(rlang))
# Symbolic objects and functions are callable:
is_callable(quote(foo))
is_callable(base::identity)

# node_poke_car() lets you modify calls without any checking:
lang <- quote(foo(10))
node_poke_car(lang, current_env())

# Use is_callable() to check an input object is safe to put as CAR:
obj <- base::identity

if (is_callable(obj)) {
  lang <- node_poke_car(lang, obj)
} else {
  abort("`obj` must be callable")
}

eval_bare(lang)