# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: na_if.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 42

suppressPackageStartupMessages(library(dplyr))
# `na_if()` is useful for replacing a single problematic value with `NA`
na_if(c(-99, 1, 4, 3, -99, 5), -99)
na_if(c("abc", "def", "", "ghi"), "")

# You can use it to standardize `NaN`s to `NA`
na_if(c(1, NaN, NA, 2, NaN), NaN)

# Because `na_if()` is an R translation of SQL's `NULLIF` command,
# it compares `x` and `y` element by element. Where `x` and `y` are
# equal, the value in `x` is replaced with an `NA`.
na_if(
  x = c(1, 2, 5, 5, 6),
  y = c(0, 2, 3, 5, 4)
)

# If you have multiple problematic values that you'd like to replace with
# `NA`, then `replace_values()` is a better choice than `na_if()`
x <- c(-99, 1, 4, 0, -99, 5, -1, 0, 5)
replace_values(x, c(0, -1, -99) ~ NA)

# You'd have to nest `na_if()`s to achieve this
try(na_if(x, c(0, -1, -99)))
na_if(na_if(na_if(x, 0), -1), -99)

# If you'd like to replace values that match a logical condition with `NA`,
# use `replace_when()`
replace_when(x, x < 0 ~ NA)

# If you'd like to replace `NA` with some other value, use `replace_values()`
x <- c(NA, 5, 2, NA, 0, 3)
replace_values(x, NA ~ 0)

# `na_if()` is particularly useful inside `mutate()`
starwars |>
  select(name, eye_color) |>
  mutate(eye_color = na_if(eye_color, "unknown"))

# `na_if()` can also be used with `mutate()` and `across()`
# to alter multiple columns
starwars |>
   mutate(across(where(is.character), ~na_if(., "unknown")))