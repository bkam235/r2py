# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_unique.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 16

suppressPackageStartupMessages(library(vctrs))
x <- rpois(100, 8)
vec_unique(x)
vec_unique_loc(x)
vec_unique_count(x)

# `vec_unique()` returns values in the order that encounters them
# use sort = "location" to match to the result of `vec_count()`
head(vec_unique(x))
head(vec_count(x, sort = "location"))

# Normally missing values are not considered to be equal
NA == NA

# But they are for the purposes of considering uniqueness
vec_unique(c(NA, NA, NA, NA, 1, 2, 1))