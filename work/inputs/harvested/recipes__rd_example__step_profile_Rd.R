# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_profile.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 53

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed(c("modeldata", "ggplot2"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

# Setup a grid across beds but keep the other values fixed
recipe(~ city + price + beds, data = Sacramento) |>
  step_profile(-beds, profile = beds) |>
  prep(training = Sacramento) |>
  bake(new_data = NULL)

##########

# An *additive* model; not for use when there are interactions or
# other functional relationships between predictors

lin_mod <- lm(mpg ~ poly(disp, 2) + cyl + hp, data = mtcars)

# Show the difference in the two grid creation methods

disp_pctl <- recipe(~ disp + cyl + hp, data = mtcars) |>
  step_profile(-disp, profile = disp) |>
  prep(training = mtcars)

disp_grid <- recipe(~ disp + cyl + hp, data = mtcars) |>
  step_profile(
    -disp,
    profile = disp,
    grid = list(pctl = FALSE, len = 100)
  ) |>
  prep(training = mtcars)

grid_data <- bake(disp_grid, new_data = NULL)
grid_data <- grid_data |>
  mutate(
    pred = predict(lin_mod, grid_data),
    method = "grid"
  )

pctl_data <- bake(disp_pctl, new_data = NULL)
pctl_data <- pctl_data |>
  mutate(
    pred = predict(lin_mod, pctl_data),
    method = "percentile"
  )

plot_data <- bind_rows(grid_data, pctl_data)

library(ggplot2)

ggplot(plot_data, aes(x = disp, y = pred)) +
  geom_point(alpha = .5, cex = 1) +
  facet_wrap(~method)
}) # examplesIf