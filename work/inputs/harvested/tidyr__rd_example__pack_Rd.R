# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: pack.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 29

suppressPackageStartupMessages(library(tidyr))
# Packing -------------------------------------------------------------------
# It's not currently clear why you would ever want to pack columns
# since few functions work with this sort of data.
df <- tibble(x1 = 1:3, x2 = 4:6, x3 = 7:9, y = 1:3)
df
df |> pack(x = starts_with("x"))
df |> pack(x = c(x1, x2, x3), y = y)

# .names_sep allows you to strip off common prefixes; this
# acts as a natural inverse to name_sep in unpack()
iris |>
  as_tibble() |>
  pack(
    Sepal = starts_with("Sepal"),
    Petal = starts_with("Petal"),
    .names_sep = "."
  )

# Unpacking -----------------------------------------------------------------
df <- tibble(
  x = 1:3,
  y = tibble(a = 1:3, b = 3:1),
  z = tibble(X = c("a", "b", "c"), Y = runif(3), Z = c(TRUE, FALSE, NA))
)
df
df |> unpack(y)
df |> unpack(c(y, z))
df |> unpack(c(y, z), names_sep = "_")