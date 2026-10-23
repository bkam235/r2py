# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: nest_by.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 21

suppressPackageStartupMessages(library(dplyr))
# After nesting, you get one row per group
iris |> nest_by(Species)
starwars |> nest_by(species)

# The output is grouped by row, which makes modelling particularly easy
models <- mtcars |>
  nest_by(cyl) |>
  mutate(model = list(lm(mpg ~ wt, data = data)))
models

models |> summarise(rsq = summary(model)$r.squared)
if (requireNamespace("broom", quietly = TRUE)) withAutoprint({ # examplesIf

# This is particularly elegant with the broom functions
models |> summarise(broom::glance(model))
models |> reframe(broom::tidy(model))
}) # examplesIf

# Note that you can also `reframe()` to unnest the data
models |> reframe(data)