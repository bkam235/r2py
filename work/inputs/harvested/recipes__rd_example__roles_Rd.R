# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: roles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 59

if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(recipes)
data(biomass, package = "modeldata")

# Using the formula method, roles are created for any outcomes and predictors:
recipe(HHV ~ ., data = biomass) |>
  summary()

# However `sample` and `dataset` aren't predictors. Since they already have
# roles, `update_role()` can be used to make changes, to any arbitrary role:
recipe(HHV ~ ., data = biomass) |>
  update_role(sample, new_role = "id variable") |>
  update_role(dataset, new_role = "splitting variable") |>
  summary()

# `update_role()` cannot set a role to NA, use `remove_role()` for that

recipe(HHV ~ ., data = biomass) |>
  update_role(sample, new_role = NA_character_)


# Variables can have more than one role. `add_role()` can be used
# if the column already has at least one role:
recipe(HHV ~ ., data = biomass) |>
  add_role(carbon, sulfur, new_role = "something") |>
  summary()

# `update_role()` has an argument called `old_role` that is required to
# unambiguously update a role when the column currently has multiple roles.
recipe(HHV ~ ., data = biomass) |>
  add_role(carbon, new_role = "something") |>
  update_role(carbon, new_role = "something else", old_role = "something") |>
  summary()

# `carbon` has two roles at the end, so the last `update_role()` fails since
# `old_role` was not given.

recipe(HHV ~ ., data = biomass) |>
  add_role(carbon, sulfur, new_role = "something") |>
  update_role(carbon, new_role = "something else")


# To remove a role, `remove_role()` can be used to remove a single role.
recipe(HHV ~ ., data = biomass) |>
  add_role(carbon, new_role = "something") |>
  remove_role(carbon, old_role = "something") |>
  summary()

# To remove all roles, call `remove_role()` multiple times to reset to `NA`
recipe(HHV ~ ., data = biomass) |>
  add_role(carbon, new_role = "something") |>
  remove_role(carbon, old_role = "something") |>
  remove_role(carbon, old_role = "predictor") |>
  summary()

# If the formula method is not used, all columns have a missing role:
recipe(biomass) |>
  summary()
}) # examplesIf