# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_rank.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 36

suppressPackageStartupMessages(library(vctrs))
x <- c(5L, 6L, 3L, 3L, 5L, 3L)

vec_rank(x, ties = "min")
vec_rank(x, ties = "max")

# Sequential ranks use an increasing sequence for duplicates
vec_rank(x, ties = "sequential")

# Dense ranks remove gaps between distinct values,
# even if there are duplicates
vec_rank(x, ties = "dense")

y <- c(NA, x, NA, NaN)

# Incomplete values match other incomplete values by default, and their
# overall position can be adjusted with `na_value`
vec_rank(y, na_value = "largest")
vec_rank(y, na_value = "smallest")

# NaN can be ranked separately from NA if required
vec_rank(y, nan_distinct = TRUE)

# Rank in descending order. Since missing values are the largest value,
# they are given a rank of `1` when ranking in descending order.
vec_rank(y, direction = "desc", na_value = "largest")

# Give incomplete values a rank of `NA` by setting `incomplete = "na"`
vec_rank(y, incomplete = "na")

# Can also rank data frames, using columns after the first to break ties
z <- c(2L, 3L, 4L, 4L, 5L, 2L)
df <- data_frame(x = x, z = z)
df

vec_rank(df)