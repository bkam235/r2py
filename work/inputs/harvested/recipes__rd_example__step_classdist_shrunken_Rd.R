# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_classdist_shrunken.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 31

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed(c("modeldata"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(penguins, package = "modeldata")
penguins <- penguins[vctrs::vec_detect_complete(penguins), ]
penguins$island <- NULL
penguins$sex <- NULL

# define naming convention
rec <- recipe(species ~ ., data = penguins) |>
  step_classdist_shrunken(all_numeric_predictors(),
    class = species,
    threshold = 1 / 4, prefix = "centroid_"
  )

# default naming
rec <- recipe(species ~ ., data = penguins) |>
  step_classdist_shrunken(all_numeric_predictors(),
    class = species,
    threshold = 3 / 4
  )

rec_dists <- prep(rec, training = penguins)

dists_to_species <- bake(rec_dists, new_data = penguins)
## on log scale:
dist_cols <- grep("classdist", names(dists_to_species), value = TRUE)
dists_to_species[, c("species", dist_cols)]

tidy(rec, number = 1)
tidy(rec_dists, number = 1)
}) # examplesIf