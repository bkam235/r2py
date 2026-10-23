# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_label.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
# as_label() is useful with quoted expressions:
as_label(expr(foo(bar)))

as_label(expr(foobar))

# It works with any R object. This is also useful for quoted
# arguments because the user might unquote constant objects:
as_label(1:3)

as_label(base::list)