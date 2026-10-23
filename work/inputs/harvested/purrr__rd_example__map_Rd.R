# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 84

suppressPackageStartupMessages(library(purrr))
# Compute normal distributions from an atomic vector
1:10 |>
  map(rnorm, n = 10)

# You can also use an anonymous function
1:10 |>
  map(\(x) rnorm(10, x))

# Simplify output to a vector instead of a list by computing the mean of the distributions
1:10 |>
  map(rnorm, n = 10) |>  # output a list
  map_dbl(mean)           # output an atomic vector

# Using set_names() with character vectors is handy to keep track
# of the original inputs:
set_names(c("foo", "bar")) |> map_chr(paste0, ":suffix")

# Working with lists
favorite_desserts <- list(Sophia = "banana bread", Eliott = "pancakes", Karina = "chocolate cake")
favorite_desserts |> map_chr(\(food) paste(food, "rocks!"))

# Extract by name or position
# .default specifies value for elements that are missing or NULL
l1 <- list(list(a = 1L), list(a = NULL, b = 2L), list(b = 3L))
l1 |> map("a", .default = "???")
l1 |> map_int("b", .default = NA)
l1 |> map_int(2, .default = NA)

# Supply multiple values to index deeply into a list
l2 <- list(
  list(num = 1:3,     letters[1:3]),
  list(num = 101:103, letters[4:6]),
  list()
)
l2 |> map(c(2, 2))

# Use a list to build an extractor that mixes numeric indices and names,
# and .default to provide a default value if the element does not exist
l2 |> map(list("num", 3))
l2 |> map_int(list("num", 3), .default = NA)

# Working with data frames
# Use map_lgl(), map_dbl(), etc to return a vector instead of a list:
mtcars |> map_dbl(sum)

# A more realistic example: split a data frame into pieces, fit a
# model to each piece, summarise and extract R^2
mtcars |>
  split(mtcars$cyl) |>
  map(\(df) lm(mpg ~ wt, data = df)) |>
  map(summary) |>
  map_dbl("r.squared")

if (interactive() && rlang::is_installed("mirai") && rlang::is_installed("carrier")) withAutoprint({ # examplesIf
# Run in interactive sessions only as spawns additional processes

# To use parallelized map:
# 1. Set daemons (number of parallel processes) first:
mirai::daemons(2)

# 2. Wrap .f with in_parallel():
mtcars |> map_dbl(in_parallel(\(x) mean(x)))

# Note that functions from packages should be fully qualified with `pkg::`
# or call `library(pkg)` within the function
1:10 |>
  map(in_parallel(\(x) vctrs::vec_init(integer(), x))) |>
  map_int(in_parallel(\(x) { library(vctrs); vec_size(x) }))

# A locally-defined function (or any required variables)
# should be passed via ... of in_parallel():
slow_lm <- function(formula, data) {
  Sys.sleep(0.5)
  lm(formula, data)
}

mtcars |>
  split(mtcars$cyl) |>
  map(in_parallel(\(df) slow_lm(mpg ~ disp, data = df), slow_lm = slow_lm))

# Tear down daemons when no longer in use:
mirai::daemons(0)
}) # examplesIf