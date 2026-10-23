# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: as_mapper.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 14

suppressPackageStartupMessages(library(purrr))
as_mapper(\(x) x + 1)
as_mapper(1)

as_mapper(c("a", "b", "c"))
# Equivalent to function(x) x[["a"]][["b"]][["c"]]

as_mapper(list(1, "a", 2))
# Equivalent to function(x) x[[1]][["a"]][[2]]

as_mapper(list(1, attr_getter("a")))
# Equivalent to function(x) attr(x[[1]], "a")

as_mapper(c("a", "b", "c"), .default = NA)