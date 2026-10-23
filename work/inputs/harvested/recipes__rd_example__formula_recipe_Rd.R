# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: formula.recipe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 7

suppressPackageStartupMessages(library(recipes))
formula(recipe(Species + Sepal.Length ~ ., data = iris) |> prep())

iris_rec <- recipe(Species ~ ., data = iris) |>
  step_center(all_numeric()) |>
  prep()
formula(iris_rec)