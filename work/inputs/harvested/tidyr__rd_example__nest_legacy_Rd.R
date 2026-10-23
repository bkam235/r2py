# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: nest_legacy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 29

suppressPackageStartupMessages(library(tidyr))
# Nest and unnest are inverses
df <- tibble(x = c(1, 1, 2), y = 3:1)
df |> nest_legacy(y)
df |> nest_legacy(y) |> unnest_legacy()

# nesting -------------------------------------------------------------------
as_tibble(iris) |> nest_legacy(!Species)
as_tibble(chickwts) |> nest_legacy(weight)

# unnesting -----------------------------------------------------------------
df <- tibble(
  x = 1:2,
  y = list(
    tibble(z = 1),
    tibble(z = 3:4)
  )
)
df |> unnest_legacy(y)

# You can also unnest multiple columns simultaneously
df <- tibble(
  a = list(c("a", "b"), "c"),
  b = list(1:2, 3),
  c = c(11, 22)
)
df |> unnest_legacy(a, b)
# If you omit the column names, it'll unnest all list-cols
df |> unnest_legacy()