# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_geodist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 19

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Smithsonian, package = "modeldata")

# How close are the museums to Union Station?
near_station <- recipe(~., data = Smithsonian) |>
  update_role(name, new_role = "location") |>
  step_geodist(
    lat = latitude, lon = longitude, log = FALSE,
    ref_lat = 38.8986312, ref_lon = -77.0062457,
    is_lat_lon = TRUE
  ) |>
  prep(training = Smithsonian)

bake(near_station, new_data = NULL) |>
  arrange(geo_dist)

tidy(near_station, number = 1)
}) # examplesIf