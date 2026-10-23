# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: context.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 15

suppressPackageStartupMessages(library(dplyr))
df <- tibble(
  g = sample(rep(letters[1:3], 1:3)),
  x = runif(6),
  y = runif(6)
)
gf <- df |> group_by(g)

gf |> summarise(n = n())

gf |> mutate(id = cur_group_id())
gf |> reframe(row = cur_group_rows())
gf |> summarise(data = list(cur_group()))

gf |> mutate(across(everything(), ~ paste(cur_column(), round(.x, 2))))