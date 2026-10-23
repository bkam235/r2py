# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: prepend.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 7

suppressPackageStartupMessages(library(purrr))
x <- as.list(1:3)

x |> append("a")
x |> prepend("a")
x |> prepend(list("a", "b"), before = 3)
prepend(list(), x)