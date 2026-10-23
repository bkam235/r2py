# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: spread.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 25

suppressPackageStartupMessages(library(tidyr))
stocks <- tibble(
  time = as.Date("2009-01-01") + 0:9,
  X = rnorm(10, 0, 1),
  Y = rnorm(10, 0, 2),
  Z = rnorm(10, 0, 4)
)
stocksm <- stocks |> gather(stock, price, -time)
stocksm |> spread(stock, price)
stocksm |> spread(time, price)

# Spread and gather are complements
df <- tibble(x = c("a", "b"), y = c(3, 4), z = c(5, 6))
df |>
  spread(x, y) |>
  gather("x", "y", a:b, na.rm = TRUE)

# Use 'convert = TRUE' to produce variables of mixed type
df <- tibble(
  row = rep(c(1, 51), each = 3),
  var = rep(c("Sepal.Length", "Species", "Species_num"), 2),
  value = c(5.1, "setosa", 1, 7.0, "versicolor", 2)
)
df |> spread(var, value) |> str()
df |> spread(var, value, convert = TRUE) |> str()