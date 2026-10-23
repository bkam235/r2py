# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 18

suppressPackageStartupMessages(library(recipes))
library(lubridate)

examples <- data.frame(
  times = ymd_hms("2022-05-06 23:51:07") +
  hours(1:5) + minutes(1:5) + seconds(1:5)
)
time_rec <- recipe(~ times, examples) |>
  step_time(all_predictors())

tidy(time_rec, number = 1)

time_rec <- prep(time_rec, training = examples)

time_values <- bake(time_rec, new_data = examples)
time_values

tidy(time_rec, number = 1)