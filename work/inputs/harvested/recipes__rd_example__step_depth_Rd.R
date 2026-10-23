# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_depth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 23

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("ddalpha")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf

# halfspace depth is the default
rec <- recipe(Species ~ ., data = iris) |>
  step_depth(all_numeric_predictors(), class = Species)

# use zonoid metric instead
# also, define naming convention for new columns
rec <- recipe(Species ~ ., data = iris) |>
  step_depth(all_numeric_predictors(),
    class = Species,
    metric = "zonoid", prefix = "zonoid_"
  )

rec_dists <- prep(rec, training = iris)

dists_to_species <- bake(rec_dists, new_data = iris)
dists_to_species

tidy(rec, number = 1)
tidy(rec_dists, number = 1)
}) # examplesIf