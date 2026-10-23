# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_locate_sorted_groups.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 11

suppressPackageStartupMessages(library(vctrs))
df <- data.frame(
  g = sample(2, 10, replace = TRUE),
  x = c(NA, sample(5, 9, replace = TRUE))
)

# `vec_locate_sorted_groups()` is similar to `vec_group_loc()`, except keys
# are returned ordered rather than by first appearance.
vec_locate_sorted_groups(df)

vec_group_loc(df)