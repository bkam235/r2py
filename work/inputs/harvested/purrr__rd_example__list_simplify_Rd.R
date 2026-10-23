# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: list_simplify.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 10

suppressPackageStartupMessages(library(purrr))
list_simplify(list(1, 2, 3))

# Only works when vectors are length one and have compatible types:
try(list_simplify(list(1, 2, 1:3)))
try(list_simplify(list(1, 2, "x")))

# Unless you strict = FALSE, in which case you get the input back:
list_simplify(list(1, 2, 1:3), strict = FALSE)
list_simplify(list(1, 2, "x"), strict = FALSE)