# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: two-table_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\two-table.R
# lines: 10

suppressPackageStartupMessages(library(dplyr))
df1 <- tibble(x = c(1, 1, 3, 4), y = 1:4)
df2 <- tibble(x = c(1, 1, 2), z = c("a", "b", "a"))

# Four rows to start with:
df1 |> nrow()
# And we get four rows after the join
df1 |> inner_join(df2, by = "x") |> nrow()
# But only two rows actually match
df1 |> semi_join(df2, by = "x") |> nrow()