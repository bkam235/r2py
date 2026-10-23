# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_rename.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 18

suppressPackageStartupMessages(library(recipes))
recipe(~., data = iris) |>
  step_rename(Sepal_Width = Sepal.Width) |>
  prep() |>
  bake(new_data = NULL) |>
  slice(1:5)

vars <- c(var1 = "cyl", var2 = "am")
car_rec <-
  recipe(~., data = mtcars) |>
  step_rename(!!!vars)

car_rec |>
  prep() |>
  bake(new_data = NULL)

car_rec |>
  tidy(number = 1)