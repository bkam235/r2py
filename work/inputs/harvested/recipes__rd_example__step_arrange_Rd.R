# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_arrange.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 39

suppressPackageStartupMessages(library(recipes))
rec <- recipe(~., data = iris) |>
  step_arrange(desc(Sepal.Length), 1 / Petal.Length)

prepped <- prep(rec, training = iris |> slice(1:75))
tidy(prepped, number = 1)

library(dplyr)

dplyr_train <-
  iris |>
  as_tibble() |>
  slice(1:75) |>
  dplyr::arrange(desc(Sepal.Length), 1 / Petal.Length)

rec_train <- bake(prepped, new_data = NULL)
all.equal(dplyr_train, rec_train)

dplyr_test <-
  iris |>
  as_tibble() |>
  slice(76:150) |>
  dplyr::arrange(desc(Sepal.Length), 1 / Petal.Length)
rec_test <- bake(prepped, iris |> slice(76:150))
all.equal(dplyr_test, rec_test)

# When you have variables/expressions, you can create a
# list of symbols with `rlang::syms()`` and splice them in
# the call with `!!!`. See https://tidyeval.tidyverse.org

sort_vars <- c("Sepal.Length", "Petal.Length")

qq_rec <-
  recipe(~., data = iris) |>
  # Embed the `values` object in the call using !!!
  step_arrange(!!!syms(sort_vars)) |>
  prep(training = iris)

tidy(qq_rec, number = 1)