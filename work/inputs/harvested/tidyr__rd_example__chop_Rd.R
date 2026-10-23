# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: chop.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 23

suppressPackageStartupMessages(library(tidyr))
# Chop ----------------------------------------------------------------------
df <- tibble(x = c(1, 1, 1, 2, 2, 3), y = 1:6, z = 6:1)
# Note that we get one row of output for each unique combination of
# non-chopped variables
df |> chop(c(y, z))
# cf nest
df |> nest(data = c(y, z))

# Unchop --------------------------------------------------------------------
df <- tibble(x = 1:4, y = list(integer(), 1L, 1:2, 1:3))
df |> unchop(y)
df |> unchop(y, keep_empty = TRUE)

# unchop will error if the types are not compatible:
df <- tibble(x = 1:2, y = list("1", 1:3))
try(df |> unchop(y))

# Unchopping a list-col of data frames must generate a df-col because
# unchop leaves the column names unchanged
df <- tibble(x = 1:3, y = list(NULL, tibble(x = 1), tibble(y = 1:2)))
df |> unchop(y)
df |> unchop(y, keep_empty = TRUE)