# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: pivot_wider_spec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 26

suppressPackageStartupMessages(library(tidyr))
# See vignette("pivot") for examples and explanation

us_rent_income
spec1 <- us_rent_income |>
  build_wider_spec(names_from = variable, values_from = c(estimate, moe))
spec1

us_rent_income |>
  pivot_wider_spec(spec1)

# Is equivalent to
us_rent_income |>
  pivot_wider(names_from = variable, values_from = c(estimate, moe))

# `pivot_wider_spec()` provides more control over column names and output format
# instead of creating columns with estimate_ and moe_ prefixes,
# keep original variable name for estimates and attach _moe as suffix
spec2 <- tibble(
  .name = c("income", "rent", "income_moe", "rent_moe"),
  .value = c("estimate", "estimate", "moe", "moe"),
  variable = c("income", "rent", "income", "rent")
)

us_rent_income |>
  pivot_wider_spec(spec2)