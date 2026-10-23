# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_slice.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 38

suppressPackageStartupMessages(library(recipes))
rec <- recipe(~., data = iris) |>
  step_slice(1:3)

prepped <- prep(rec, training = iris |> slice(1:75))
tidy(prepped, number = 1)

library(dplyr)

dplyr_train <-
  iris |>
  as_tibble() |>
  slice(1:75) |>
  slice(1:3)

rec_train <- bake(prepped, new_data = NULL)
all.equal(dplyr_train, rec_train)

dplyr_test <-
  iris |>
  as_tibble() |>
  slice(76:150)

rec_test <- bake(prepped, iris |> slice(76:150))
all.equal(dplyr_test, rec_test)

# Embedding the integer expression (or vector) into the
# recipe:

keep_rows <- 1:6

qq_rec <-
  recipe(~., data = iris) |>
  # Embed `keep_rows` in the call using !!!
  step_slice(!!!keep_rows) |>
  prep(training = iris)

tidy(qq_rec, number = 1)