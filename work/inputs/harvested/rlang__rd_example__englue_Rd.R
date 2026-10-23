# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: englue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 10

suppressPackageStartupMessages(library(rlang))
g <- function(var) englue("{{ var }}")
g(cyl)
g(1 + 1)
g(!!letters)

# These are equivalent to
as_label(quote(cyl))
as_label(quote(1 + 1))
as_label(letters)