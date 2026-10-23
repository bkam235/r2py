# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_interact.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 27

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(penguins, package = "modeldata")
penguins <- penguins |> na.omit()

rec <- recipe(flipper_length_mm ~ ., data = penguins)

int_mod_1 <- rec |>
  step_interact(terms = ~ bill_depth_mm:bill_length_mm)

# specify all dummy variables succinctly with `starts_with()`
int_mod_2 <- rec |>
  step_dummy(sex, species, island) |>
  step_interact(terms = ~ body_mass_g:starts_with("species"))

int_mod_1 <- prep(int_mod_1, training = penguins)
int_mod_2 <- prep(int_mod_2, training = penguins)

dat_1 <- bake(int_mod_1, penguins)
dat_2 <- bake(int_mod_2, penguins)

names(dat_1)
names(dat_2)

tidy(int_mod_1, number = 1)
tidy(int_mod_2, number = 2)
}) # examplesIf