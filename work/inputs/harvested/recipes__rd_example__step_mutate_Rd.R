# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_mutate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 66

suppressPackageStartupMessages(library(recipes))
rec <-
  recipe(~., data = iris) |>
  step_mutate(
    dbl_width = Sepal.Width * 2,
    half_length = Sepal.Length / 2
  )

prepped <- prep(rec, training = iris |> slice(1:75))

library(dplyr)

dplyr_train <-
  iris |>
  as_tibble() |>
  slice(1:75) |>
  mutate(
    dbl_width = Sepal.Width * 2,
    half_length = Sepal.Length / 2
  )

rec_train <- bake(prepped, new_data = NULL)
all.equal(dplyr_train, rec_train)

dplyr_test <-
  iris |>
  as_tibble() |>
  slice(76:150) |>
  mutate(
    dbl_width = Sepal.Width * 2,
    half_length = Sepal.Length / 2
  )
rec_test <- bake(prepped, iris |> slice(76:150))
all.equal(dplyr_test, rec_test)

# Embedding objects:
const <- 1.414

qq_rec <-
  recipe(~., data = iris) |>
  step_mutate(
    bad_approach = Sepal.Width * const,
    best_approach = Sepal.Width * !!const
  ) |>
  prep(training = iris)

bake(qq_rec, new_data = NULL, contains("appro")) |> slice(1:4)

# The difference:
tidy(qq_rec, number = 1)

# Using across()
recipe(~., data = iris) |>
  step_mutate(across(contains("Length"), .fns = ~ 1 / .)) |>
  prep() |>
  bake(new_data = NULL) |>
  slice(1:10)

recipe(~., data = iris) |>
  # leads to more columns being created.
  step_mutate(
    across(contains("Length"), .fns = list(log = log, sqrt = sqrt))
  ) |>
  prep() |>
  bake(new_data = NULL) |>
  slice(1:10)