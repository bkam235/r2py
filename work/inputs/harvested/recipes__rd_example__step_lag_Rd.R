# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_lag.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 15

suppressPackageStartupMessages(library(recipes))
n <- 10
start <- as.Date("1999/01/01")
end <- as.Date("1999/01/10")

df <- data.frame(
  x = runif(n),
  index = 1:n,
  day = seq(start, end, by = "day")
)

recipe(~., data = df) |>
  step_lag(index, day, lag = 2:3) |>
  prep(df) |>
  bake(df)