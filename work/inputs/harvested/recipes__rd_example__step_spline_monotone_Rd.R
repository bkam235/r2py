# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_spline_monotone.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 24

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed(c("modeldata", "ggplot2"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(tidyr)
library(dplyr)

library(ggplot2)
data(ames, package = "modeldata")

spline_rec <- recipe(Sale_Price ~ Longitude, data = ames) |>
  step_spline_monotone(Longitude, deg_free = 6, keep_original_cols = TRUE) |>
  prep()

tidy(spline_rec, number = 1)

# Show where each feature is active
spline_rec |>
  bake(new_data =  NULL,-Sale_Price) |>
  pivot_longer(c(starts_with("Longitude_")), names_to = "feature", values_to = "value") |>
  mutate(feature = gsub("Longitude_", "feature ", feature)) |>
  filter(value > 0) |>
  ggplot(aes(x = Longitude, y = value)) +
  geom_line() +
  facet_wrap(~ feature)
}) # examplesIf