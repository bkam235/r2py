# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: pivot_longer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 39

suppressPackageStartupMessages(library(tidyr))
# See vignette("pivot") for examples and explanation

# Simplest case where column names are character data
relig_income
relig_income |>
  pivot_longer(!religion, names_to = "income", values_to = "count")

# Slightly more complex case where columns have common prefix,
# and missing missings are structural so should be dropped.
billboard
billboard |>
  pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    names_prefix = "wk",
    values_to = "rank",
    values_drop_na = TRUE
  )

# Multiple variables stored in column names
who |> pivot_longer(
  cols = new_sp_m014:newrel_f65,
  names_to = c("diagnosis", "gender", "age"),
  names_pattern = "new_?(.*)_(.)(.*)",
  values_to = "count"
)

# Multiple observations per row. Since all columns are used in the pivoting
# process, we'll use `cols_vary` to keep values from the original columns
# close together in the output.
anscombe
anscombe |>
  pivot_longer(
    everything(),
    cols_vary = "slowest",
    names_to = c(".value", "set"),
    names_pattern = "(.)(.)"
  )