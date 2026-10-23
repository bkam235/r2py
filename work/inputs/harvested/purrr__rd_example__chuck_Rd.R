# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: chuck.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 11

suppressPackageStartupMessages(library(purrr))
x <- list(a = 1, b = 2)

# When indexing an element that doesn't exist `[[` sometimes returns NULL:
x[["y"]]
# and sometimes errors:
try(x[[3]])

# chuck() consistently errors:
try(chuck(x, "y"))
try(chuck(x, 3))