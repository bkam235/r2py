# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: expr_print.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 26

suppressPackageStartupMessages(library(rlang))
# It supports any object. Non-symbolic objects are always printed
# within angular brackets:
expr_print(1:3)
expr_print(function() NULL)

# Contrast this to how the code to create these objects is printed:
expr_print(quote(1:3))
expr_print(quote(function() NULL))

# The main cause of non-symbolic objects in expressions is
# quasiquotation:
expr_print(expr(foo(!!(1:3))))


# Quosures from the global environment are printed normally:
expr_print(quo(foo))
expr_print(quo(foo(!!quo(bar))))

# Quosures from local environments are colourised according to
# their environments (if you have crayon installed):
local_quo <- local(quo(foo))
expr_print(local_quo)

wrapper_quo <- local(quo(bar(!!local_quo, baz)))
expr_print(wrapper_quo)