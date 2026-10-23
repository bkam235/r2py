# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: pivot_longer_spec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 20

suppressPackageStartupMessages(library(tidyr))
# See vignette("pivot") for examples and explanation

# Use `build_longer_spec()` to build `spec` using similar syntax to `pivot_longer()`
# and run `pivot_longer_spec()` based on `spec`.
spec <- relig_income |> build_longer_spec(
  cols = !religion,
  names_to = "income",
  values_to = "count"
)
spec

pivot_longer_spec(relig_income, spec)

# Is equivalent to:
relig_income |> pivot_longer(
  cols = !religion,
  names_to = "income",
  values_to = "count"
)