# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_if_else.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 17

suppressPackageStartupMessages(library(vctrs))
x <- c(-5:5, NA)
vec_if_else(x < 0, NA, x)

# Explicitly handle `NA` values in the `condition` with `missing`
vec_if_else(x < 0, "negative", "positive", missing = "missing")

# Unlike `ifelse()`, `vec_if_else()` preserves types
x <- factor(sample(letters[1:5], 10, replace = TRUE))
ifelse(x %in% c("a", "b", "c"), x, NA)
vec_if_else(x %in% c("a", "b", "c"), x, NA)

# `vec_if_else()` also works with data frames
condition <- c(TRUE, FALSE, NA, TRUE)
true <- data_frame(x = 1:4, y = 5:8)
false <- data_frame(x = 9:12, y = 13:16)
vec_if_else(condition, true, false)