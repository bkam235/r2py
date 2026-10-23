# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_closure.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 9

suppressPackageStartupMessages(library(rlang))
# Primitive functions are regularised as closures
as_closure(list)
as_closure("list")

# Operators have `.x` and `.y` as arguments, just like lambda
# functions created with the formula syntax:
as_closure(`+`)
as_closure(`~`)