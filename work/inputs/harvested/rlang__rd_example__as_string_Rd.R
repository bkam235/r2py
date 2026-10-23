# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_string.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
# Let's create some symbols:
foo <- quote(foo)
bar <- sym("bar")

# as_string() converts symbols to strings:
foo
as_string(foo)

typeof(bar)
typeof(as_string(bar))