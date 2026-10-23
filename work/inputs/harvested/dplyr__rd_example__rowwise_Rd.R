# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: rowwise.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 30

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = runif(6), y = runif(6), z = runif(6))
# Compute the mean of x, y, z in each row
df |> rowwise() |> mutate(m = mean(c(x, y, z)))
# use c_across() to more easily select many variables
df |> rowwise() |> mutate(m = mean(c_across(x:z)))

# Compute the minimum of x and y in each row
df |> rowwise() |> mutate(m = min(c(x, y, z)))
# In this case you can use an existing vectorised function:
df |> mutate(m = pmin(x, y, z))
# Where these functions exist they'll be much faster than rowwise
# so be on the lookout for them.

# rowwise() is also useful when doing simulations
params <- tribble(
 ~sim, ~n, ~mean, ~sd,
    1,  1,     1,   1,
    2,  2,     2,   4,
    3,  3,    -1,   2
)
# Here I supply variables to preserve after the computation
params |>
  rowwise(sim) |>
  reframe(z = rnorm(n, mean, sd))

# If you want one row per simulation, put the results in a list()
params |>
  rowwise(sim) |>
  summarise(z = list(rnorm(n, mean, sd)), .groups = "keep")