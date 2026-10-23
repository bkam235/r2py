# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: coalesce.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 37

suppressPackageStartupMessages(library(dplyr))
# Replace missing values with a single value
x <- sample(c(1:5, NA, NA, NA))
coalesce(x, 0L)

# Or replace missing values with the corresponding non-missing value in
# another vector
x <- c(1, 2, NA, NA, 5, NA)
y <- c(NA, NA, 3, 4, 5, NA)
coalesce(x, y)

# For cases like these where your replacement is a single value or a single
# vector, `replace_values()` works just as well
replace_values(x, NA ~ 0)
coalesce(x, 0)

replace_values(x, NA ~ y)
coalesce(x, y)

# `coalesce()` really shines when you have >2 vectors to coalesce with
z <- c(NA, 2, 3, 4, 5, 6)
coalesce(x, y, z)

# If you're looking to replace values with `NA`, rather than replacing `NA`
# with a value, then use `replace_values()`
x <- c(0, -1, 5, -99, 8)
replace_values(x, c(-1, -99) ~ NA)

# The equivalent to a missing value in a list is `NULL`
coalesce(list(1, 2, NULL, NA), list(0))

# Supply lists of vectors by splicing them into dots
vecs <- list(
  c(1, 2, NA, NA, 5),
  c(NA, NA, 3, 4, 5)
)
coalesce(!!!vecs)