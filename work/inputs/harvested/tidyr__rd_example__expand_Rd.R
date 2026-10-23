# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: expand.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 41

suppressPackageStartupMessages(library(tidyr))
# Finding combinations ------------------------------------------------------
fruits <- tibble(
  type = c("apple", "orange", "apple", "orange", "orange", "orange"),
  year = c(2010, 2010, 2012, 2010, 2011, 2012),
  size = factor(
    c("XS", "S", "M", "S", "S", "M"),
    levels = c("XS", "S", "M", "L")
  ),
  weights = rnorm(6, as.numeric(size) + 2)
)

# All combinations, including factor levels that are not used
fruits |> expand(type)
fruits |> expand(size)
fruits |> expand(type, size)
fruits |> expand(type, size, year)

# Only combinations that already appear in the data
fruits |> expand(nesting(type))
fruits |> expand(nesting(size))
fruits |> expand(nesting(type, size))
fruits |> expand(nesting(type, size, year))

# Other uses ----------------------------------------------------------------
# Use with `full_seq()` to fill in values of continuous variables
fruits |> expand(type, size, full_seq(year, 1))
fruits |> expand(type, size, 2010:2013)

# Use `anti_join()` to determine which observations are missing
all <- fruits |> expand(type, size, year)
all
all |> dplyr::anti_join(fruits)

# Use with `right_join()` to fill in missing rows (like `complete()`)
fruits |> dplyr::right_join(all)

# Use with `group_by()` to expand within each group
fruits |>
  dplyr::group_by(type) |>
  expand(year, size)