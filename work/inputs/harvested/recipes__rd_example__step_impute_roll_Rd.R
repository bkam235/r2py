# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_impute_roll.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 21

library(lubridate)

set.seed(145)
example_data <-
  data.frame(
    day = ymd("2012-06-07") + days(1:12),
    x1 = round(runif(12), 2),
    x2 = round(runif(12), 2),
    x3 = round(runif(12), 2)
  )
example_data$x1[c(1, 5, 6)] <- NA
example_data$x2[c(1:4, 10)] <- NA

library(recipes)
seven_pt <- recipe(~., data = example_data) |>
  update_role(day, new_role = "time_index") |>
  step_impute_roll(all_numeric_predictors(), window = 7) |>
  prep(training = example_data)

# The training set:
bake(seven_pt, new_data = NULL)