# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: list_transpose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 33

suppressPackageStartupMessages(library(purrr))
# list_transpose() is useful in conjunction with safely()
x <- list("a", 1, 2)
y <- x |> map(safely(log))
y |> str()
# Put all the errors and results together
y |> list_transpose() |> str()
# Supply a default result to further simplify
y |> list_transpose(default = list(result = NA)) |> str()

# list_transpose() will try to simplify by default:
x <- list(list(a = 1, b = 2), list(a = 3, b = 4), list(a = 5, b = 6))
x |> list_transpose()
# this makes list_tranpose() not completely symmetric
x |> list_transpose() |> list_transpose()

# use simplify = FALSE to always return lists:
x |> list_transpose(simplify = FALSE) |> str()
x |>
  list_transpose(simplify = FALSE) |>
  list_transpose(simplify = FALSE) |> str()

# Provide an explicit template if you know which elements you want to extract
ll <- list(
  list(x = 1, y = "one"),
  list(z = "deux", x = 2)
)
ll |> list_transpose()
ll |> list_transpose(template = c("x", "y", "z"))
ll |> list_transpose(template = 1)

# And specify a default if you want to simplify
ll |> list_transpose(template = c("x", "y", "z"), default = NA)