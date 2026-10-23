# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: nth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 45

suppressPackageStartupMessages(library(dplyr))
x <- 1:10
y <- 10:1

first(x)
last(y)

nth(x, 1)
nth(x, 5)
nth(x, -2)

# `first()` and `last()` are often useful in `summarise()`
df <- tibble(x = x, y = y)
df |>
  summarise(
    across(x:y, first, .names = "{col}_first"),
    y_last = last(y)
  )

# Selecting a position that is out of bounds returns a default value
nth(x, 11)
nth(x, 0)

# This out of bounds behavior also applies to empty vectors
first(integer())

# You can customize the default value with `default`
nth(x, 11, default = -1L)
first(integer(), default = 0L)

# `order_by` provides optional ordering
last(x)
last(x, order_by = y)

# `na_rm` removes missing values before extracting the value
z <- c(NA, NA, 1, 3, NA, 5, NA)
first(z)
first(z, na_rm = TRUE)
last(z, na_rm = TRUE)
nth(z, 3, na_rm = TRUE)

# For data frames, these select entire rows
df <- tibble(a = 1:5, b = 6:10)
first(df)
nth(df, 4)