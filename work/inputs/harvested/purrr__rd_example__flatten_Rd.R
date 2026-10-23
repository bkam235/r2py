# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: flatten.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 14

suppressPackageStartupMessages(library(purrr))
x <- map(1:3, \(i) sample(4))
x

# was
x |> flatten_int() |> str()
# now
x |> list_c() |> str()

x <- list(list(1, 2), list(3, 4))
# was
x |> flatten() |> str()
# now
x |> list_flatten() |> str()