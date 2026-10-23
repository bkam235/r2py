# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_dummy_extract.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 48

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(tate_text, package = "modeldata")

dummies <- recipe(~ artist + medium, data = tate_text) |>
  step_dummy_extract(artist, medium, sep = ", ") |>
  prep()

dummy_data <- bake(dummies, new_data = NULL)

dummy_data |>
  select(starts_with("medium")) |>
  names() |>
  head()

# More detailed splitting
dummies_specific <- recipe(~medium, data = tate_text) |>
  step_dummy_extract(medium, sep = "(, )|( and )|( on )") |>
  prep()

dummy_data_specific <- bake(dummies_specific, new_data = NULL)

dummy_data_specific |>
  select(starts_with("medium")) |>
  names() |>
  head()

tidy(dummies, number = 1)
tidy(dummies_specific, number = 1)

# pattern argument can be useful to extract harder patterns
color_examples <- tibble(
  colors = c(
    "['red', 'blue']",
    "['red', 'blue', 'white']",
    "['blue', 'blue', 'blue']"
  )
)

dummies_color <- recipe(~colors, data = color_examples) |>
  step_dummy_extract(colors, pattern = "(?<=')[^',]+(?=')") |>
  prep()

dummies_data_color <- dummies_color |>
  bake(new_data = NULL)

dummies_data_color
}) # examplesIf