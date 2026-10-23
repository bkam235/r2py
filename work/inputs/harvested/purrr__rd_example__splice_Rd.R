# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: splice.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 7

suppressPackageStartupMessages(library(purrr))
inputs <- list(arg1 = "a", arg2 = "b")

# splice() concatenates the elements of inputs with arg3
splice(inputs, arg3 = c("c1", "c2")) |> str()
list(inputs, arg3 = c("c1", "c2")) |> str()
c(inputs, arg3 = c("c1", "c2")) |> str()