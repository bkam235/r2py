# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: list_flatten.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 37

suppressPackageStartupMessages(library(purrr))
x <- list(1, list(2, 3), list(4, list(5)))
x |> list_flatten() |> str()
x |> list_flatten() |> list_flatten() |> str()

# Flat lists are left as is
list(1, 2, 3, 4, 5) |> list_flatten() |> str()

# Empty lists will disappear
list(1, list(), 2, list(3)) |> list_flatten() |> str()

# Another way to see this is that it reduces the depth of the list
x <- list(
  list(),
  list(list())
)
x |> pluck_depth()
x |> list_flatten() |> pluck_depth()

# Use name_spec to control how inner and outer names are combined
x <- list(x = list(a = 1, b = 2), y = list(c = 1, d = 2))
x |> list_flatten() |> names()
x |> list_flatten(name_spec = "{outer}") |> names()
x |> list_flatten(name_spec = "{inner}") |> names()

# Set `is_node = is.list` to also flatten richer objects built on lists like
# data frames and linear models
df <- data.frame(x = 1:3, y = 4:6)
x <- list(
  a_string = "something",
  a_list = list(1:3, "else"),
  a_df = df
)
x |> list_flatten(is_node = is.list)

# Note that objects that are already "flat" retain their classes
list_flatten(df, is_node = is.list)