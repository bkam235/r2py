# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: quosure-tools.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 30

suppressPackageStartupMessages(library(rlang))
quo <- quo(my_quosure)
quo


# Access and set the components of a quosure:
quo_get_expr(quo)
quo_get_env(quo)

quo <- quo_set_expr(quo, quote(baz))
quo <- quo_set_env(quo, empty_env())
quo

# Test wether an object is a quosure:
is_quosure(quo)

# If it is a quosure, you can use the specialised type predicates
# to check what is inside it:
quo_is_symbol(quo)
quo_is_call(quo)
quo_is_null(quo)

# quo_is_missing() checks for a special kind of quosure, the one
# that contains the missing argument:
quo()
quo_is_missing(quo())

fn <- function(arg) enquo(arg)
fn()
quo_is_missing(fn())