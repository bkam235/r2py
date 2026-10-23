# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: keep_at.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 8

suppressPackageStartupMessages(library(purrr))
x <- c(a = 1, b = 2, cat = 10, dog = 15, elephant = 5, e = 10)
x |> keep_at(letters)
x |> discard_at(letters)

# Can also use a function
x |> keep_at(\(x) nchar(x) == 3)
x |> discard_at(\(x) nchar(x) == 3)