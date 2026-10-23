# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: distinct_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 20

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = rep(2:5, each = 2) / 2, y = rep(2:3, each = 4) / 2)

distinct_all(df)
# ->
distinct(df, pick(everything()))

distinct_at(df, vars(x,y))
# ->
distinct(df, pick(x, y))

distinct_if(df, is.numeric)
# ->
distinct(df, pick(where(is.numeric)))

# You can supply a function that will be applied before extracting the distinct values
# The variables of the sorted tibble keep their original values.
distinct_all(df, round)
# ->
distinct(df, across(everything(), round))