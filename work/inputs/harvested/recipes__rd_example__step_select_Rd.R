# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_select.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 32

suppressPackageStartupMessages(library(recipes))
library(dplyr)

iris_tbl <- as_tibble(iris)
iris_train <- slice(iris_tbl, 1:75)
iris_test <- slice(iris_tbl, 76:150)

dplyr_train <- select(iris_train, Species, starts_with("Sepal"))
dplyr_test <- select(iris_test, Species, starts_with("Sepal"))

rec <- recipe(~., data = iris_train) |>
  step_select(Species, starts_with("Sepal")) |>
  prep(training = iris_train)

rec_train <- bake(rec, new_data = NULL)
all.equal(dplyr_train, rec_train)

rec_test <- bake(rec, iris_test)
all.equal(dplyr_test, rec_test)

# Local variables
sepal_vars <- c("Sepal.Width", "Sepal.Length")

qq_rec <-
  recipe(~., data = iris_train) |>
  # fine for interactive usage
  step_select(Species, all_of(sepal_vars)) |>
  # best approach for saving a recipe to disk
  step_select(Species, all_of(!!sepal_vars))

# Note that `sepal_vars` is inlined in the second approach
qq_rec