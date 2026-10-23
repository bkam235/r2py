# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: default_recipe_blueprint.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 95

suppressPackageStartupMessages(library(hardhat))
if (rlang::is_installed(c("recipes"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# example code

library(recipes)

# ---------------------------------------------------------------------------
# Setup

train <- iris[1:100, ]
test <- iris[101:150, ]

# ---------------------------------------------------------------------------
# Recipes example

# Create a recipe that logs a predictor
rec <- recipe(Species ~ Sepal.Length + Sepal.Width, train) |>
  step_log(Sepal.Length)

processed <- mold(rec, train)

# Sepal.Length has been logged
processed$predictors

processed$outcomes

# The underlying blueprint is a prepped recipe
processed$blueprint$recipe

# Call forge() with the blueprint and the test data
# to have it preprocess the test data in the same way
forge(test, processed$blueprint)

# Use `outcomes = TRUE` to also extract the preprocessed outcome!
# This logged the Sepal.Length column of `new_data`
forge(test, processed$blueprint, outcomes = TRUE)

# ---------------------------------------------------------------------------
# With an intercept

# You can add an intercept with `intercept = TRUE`
processed <- mold(rec, train, blueprint = default_recipe_blueprint(intercept = TRUE))

processed$predictors

# But you also could have used a recipe step
rec2 <- step_intercept(rec)

mold(rec2, iris)$predictors

# ---------------------------------------------------------------------------
# Matrix output for predictors

# You can change the `composition` of the predictor data set
bp <- default_recipe_blueprint(composition = "dgCMatrix")
processed <- mold(rec, train, blueprint = bp)
class(processed$predictors)

# ---------------------------------------------------------------------------
# Non standard roles

# If you have custom recipes roles, they are assumed to be required at
# `bake()` time when passing in `new_data`. This is an assumption that both
# recipes and hardhat makes, meaning that those roles are required at
# `forge()` time as well.
rec_roles <- recipe(train) |>
  update_role(Sepal.Width, new_role = "predictor") |>
  update_role(Species, new_role = "outcome") |>
  update_role(Sepal.Length, new_role = "id") |>
  update_role(Petal.Length, new_role = "important")

processed_roles <- mold(rec_roles, train)

# The custom roles will be in the `mold()` result in case you need
# them for modeling.
processed_roles$extras

# And they are in the `forge()` result
forge(test, processed_roles$blueprint)$extras

# If you remove a column with a custom role from the test data, then you
# won't be able to `forge()` even though this recipe technically didn't
# use that column in any steps
test2 <- test
test2$Petal.Length <- NULL
try(forge(test2, processed_roles$blueprint))

# Most of the time, if you find yourself in the above scenario, then we
# suggest that you remove `Petal.Length` from the data that is supplied to
# the recipe. If that isn't an option, you can declare that that column
# isn't required at `bake()` time by using `update_role_requirements()`
rec_roles <- update_role_requirements(rec_roles, "important", bake = FALSE)
processed_roles <- mold(rec_roles, train)
forge(test2, processed_roles$blueprint)
}) # examplesIf