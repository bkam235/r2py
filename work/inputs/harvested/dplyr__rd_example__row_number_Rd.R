# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: row_number.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 27

suppressPackageStartupMessages(library(dplyr))
x <- c(5, 1, 3, 2, 2, NA)
row_number(x)
min_rank(x)
dense_rank(x)

# Ranking functions can be used in `filter()` to select top/bottom rows
df <- data.frame(
  grp = c(1, 1, 1, 2, 2, 2, 3, 3, 3),
  x = c(3, 2, 1, 1, 2, 2, 1, 1, 1),
  y = c(1, 3, 2, 3, 2, 2, 4, 1, 2),
  id = 1:9
)
# Always gives exactly 1 row per group
df |> group_by(grp) |> filter(row_number(x) == 1)
# May give more than 1 row if ties
df |> group_by(grp) |> filter(min_rank(x) == 1)
# Rank by multiple columns (to break ties) by selecting them with `pick()`
df |> group_by(grp) |> filter(min_rank(pick(x, y)) == 1)
# See slice_min() and slice_max() for another way to tackle the same problem

# You can use row_number() without an argument to refer to the "current"
# row number.
df |> group_by(grp) |> filter(row_number() == 1)

# It's easiest to see what this does with mutate():
df |> group_by(grp) |> mutate(grp_id = row_number())