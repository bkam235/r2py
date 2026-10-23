# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: summarise_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 34

suppressPackageStartupMessages(library(dplyr))
# The _at() variants directly support strings:
starwars |>
  summarise_at(c("height", "mass"), mean, na.rm = TRUE)
# ->
starwars |> summarise(across(c("height", "mass"), ~ mean(.x, na.rm = TRUE)))

# You can also supply selection helpers to _at() functions but you have
# to quote them with vars():
starwars |>
  summarise_at(vars(height:mass), mean, na.rm = TRUE)
# ->
starwars |>
  summarise(across(height:mass, ~ mean(.x, na.rm = TRUE)))

# The _if() variants apply a predicate function (a function that
# returns TRUE or FALSE) to determine the relevant subset of
# columns. Here we apply mean() to the numeric columns:
starwars |>
  summarise_if(is.numeric, mean, na.rm = TRUE)
starwars |>
  summarise(across(where(is.numeric), ~ mean(.x, na.rm = TRUE)))

by_species <- iris |>
  group_by(Species)

# If you want to apply multiple transformations, pass a list of
# functions. When there are multiple functions, they create new
# variables instead of modifying the variables in place:
by_species |>
  summarise_all(list(min, max))
# ->
by_species |>
  summarise(across(everything(), list(min = min, max = max)))