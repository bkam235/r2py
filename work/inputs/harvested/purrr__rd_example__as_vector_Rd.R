# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: as_vector.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 10

suppressPackageStartupMessages(library(purrr))
# was
as.list(letters) |> as_vector("character")
# now
as.list(letters) |> list_simplify(ptype = character())

# was:
list(1:2, 3:4, 5:6) |> as_vector(integer(2))
# now:
list(1:2, 3:4, 5:6) |> list_c(ptype = integer())