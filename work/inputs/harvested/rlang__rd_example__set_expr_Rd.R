# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: set_expr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
f <- ~foo(bar)
e <- quote(foo(bar))
frame <- identity(identity(ctxt_frame()))

get_expr(f)
get_expr(e)
get_expr(frame)

set_expr(f, quote(baz))
set_expr(e, quote(baz))