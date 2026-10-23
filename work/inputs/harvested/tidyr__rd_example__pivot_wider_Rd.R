# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: pivot_wider.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 61

suppressPackageStartupMessages(library(tidyr))
# See vignette("pivot") for examples and explanation

fish_encounters
fish_encounters |>
  pivot_wider(names_from = station, values_from = seen)
# Fill in missing values
fish_encounters |>
  pivot_wider(names_from = station, values_from = seen, values_fill = 0)

# Generate column names from multiple variables
us_rent_income
us_rent_income |>
  pivot_wider(
    names_from = variable,
    values_from = c(estimate, moe)
  )

# You can control whether `names_from` values vary fastest or slowest
# relative to the `values_from` column names using `names_vary`.
us_rent_income |>
  pivot_wider(
    names_from = variable,
    values_from = c(estimate, moe),
    names_vary = "slowest"
  )

# When there are multiple `names_from` or `values_from`, you can use
# use `names_sep` or `names_glue` to control the output variable names
us_rent_income |>
  pivot_wider(
    names_from = variable,
    names_sep = ".",
    values_from = c(estimate, moe)
  )
us_rent_income |>
  pivot_wider(
    names_from = variable,
    names_glue = "{variable}_{.value}",
    values_from = c(estimate, moe)
  )

# Can perform aggregation with `values_fn`
warpbreaks <- as_tibble(warpbreaks[c("wool", "tension", "breaks")])
warpbreaks
warpbreaks |>
  pivot_wider(
    names_from = wool,
    values_from = breaks,
    values_fn = mean
  )

# Can pass an anonymous function to `values_fn` when you
# need to supply additional arguments
warpbreaks$breaks[1] <- NA
warpbreaks |>
  pivot_wider(
    names_from = wool,
    values_from = breaks,
    values_fn = ~ mean(.x, na.rm = TRUE)
  )