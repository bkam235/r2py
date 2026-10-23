# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: nest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 44

suppressPackageStartupMessages(library(tidyr))
df <- tibble(x = c(1, 1, 1, 2, 2, 3), y = 1:6, z = 6:1)

# Specify variables to nest using name-variable pairs.
# Note that we get one row of output for each unique combination of
# non-nested variables.
df |> nest(data = c(y, z))

# Specify variables to nest by (rather than variables to nest) using `.by`
df |> nest(.by = x)

# In this case, since `...` isn't used you can specify the resulting column
# name with `.key`
df |> nest(.by = x, .key = "cols")

# Use tidyselect syntax and helpers, just like in `dplyr::select()`
df |> nest(data = any_of(c("y", "z")))

# `...` and `.by` can be used together to drop columns you no longer need,
# or to include the columns you are nesting by in the inner data frame too.
# This drops `z`:
df |> nest(data = y, .by = x)
# This includes `x` in the inner data frame:
df |> nest(data = everything(), .by = x)

# Multiple nesting structures can be specified at once
iris |>
  nest(petal = starts_with("Petal"), sepal = starts_with("Sepal"))
iris |>
  nest(width = contains("Width"), length = contains("Length"))

# Nesting a grouped data frame nests all variables apart from the group vars
fish_encounters |>
  dplyr::group_by(fish) |>
  nest()

# That is similar to `nest(.by = )`, except here the result isn't grouped
fish_encounters |>
  nest(.by = fish)

# Nesting is often useful for creating per group models
mtcars |>
  nest(.by = cyl) |>
  dplyr::mutate(models = lapply(data, function(df) lm(mpg ~ wt, data = df)))