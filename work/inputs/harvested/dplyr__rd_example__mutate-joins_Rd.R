# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: mutate-joins.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 47

suppressPackageStartupMessages(library(dplyr))
band_members |> inner_join(band_instruments)
band_members |> left_join(band_instruments)
band_members |> right_join(band_instruments)
band_members |> full_join(band_instruments)

# To suppress the message about joining variables, supply `by`
band_members |> inner_join(band_instruments, by = join_by(name))
# This is good practice in production code

# Use an equality expression if the join variables have different names
band_members |> full_join(band_instruments2, by = join_by(name == artist))
# By default, the join keys from `x` and `y` are coalesced in the output; use
# `keep = TRUE` to keep the join keys from both `x` and `y`
band_members |>
  full_join(band_instruments2, by = join_by(name == artist), keep = TRUE)

# If a row in `x` matches multiple rows in `y`, all the rows in `y` will be
# returned once for each matching row in `x`.
df1 <- tibble(x = 1:3)
df2 <- tibble(x = c(1, 1, 2), y = c("first", "second", "third"))
df1 |> left_join(df2)

# If a row in `y` also matches multiple rows in `x`, this is known as a
# many-to-many relationship, which is typically a result of an improperly
# specified join or some kind of messy data. In this case, a warning is
# thrown by default:
df3 <- tibble(x = c(1, 1, 1, 3))
df3 |> left_join(df2)

# In the rare case where a many-to-many relationship is expected, set
# `relationship = "many-to-many"` to silence this warning
df3 |> left_join(df2, relationship = "many-to-many")

# Use `join_by()` with a condition other than `==` to perform an inequality
# join. Here we match on every instance where `df1$x > df2$x`.
df1 |> left_join(df2, join_by(x > x))

# By default, NAs match other NAs so that there are two
# rows in the output of this join:
df1 <- data.frame(x = c(1, NA), y = 2)
df2 <- data.frame(x = c(1, NA), z = 3)
left_join(df1, df2)

# You can optionally request that NAs don't match, giving a
# a result that more closely resembles SQL joins
left_join(df1, df2, na_matches = "never")