# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_name.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 14

suppressPackageStartupMessages(library(rlang))
# Let's create some symbols:
foo <- quote(foo)
bar <- sym("bar")

# as_name() converts symbols to strings:
foo
as_name(foo)

typeof(bar)
typeof(as_name(bar))

# as_name() unwraps quosured symbols automatically:
as_name(quo(foo))