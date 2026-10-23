# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Skipping_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Skipping.R
# lines: 9

library(recipes)
car_recipe <- recipe(mpg ~ ., data = mtcars) |>
  step_log(disp, skip = TRUE) |>
  step_center(all_numeric_predictors()) |>
  prep(training = mtcars)

# These *should* produce the same results (as they do for `hp`)
bake(car_recipe, new_data = NULL)   |> head() |> select(disp, hp)
bake(car_recipe, new_data = mtcars) |> head() |> select(disp, hp)