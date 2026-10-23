# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 56

suppressPackageStartupMessages(library(dplyr))
# return a list
mtcars |>
  group_by(cyl) |>
  group_map(~ head(.x, 2L))

# return a tibble grouped by `cyl` with 2 rows per group
# the grouping data is recalculated
mtcars |>
  group_by(cyl) |>
  group_modify(~ head(.x, 2L))
if (requireNamespace("broom", quietly = TRUE)) withAutoprint({ # examplesIf

# a list of tibbles
iris |>
  group_by(Species) |>
  group_map(~ broom::tidy(lm(Petal.Length ~ Sepal.Length, data = .x)))

# a restructured grouped tibble
iris |>
  group_by(Species) |>
  group_modify(~ broom::tidy(lm(Petal.Length ~ Sepal.Length, data = .x)))
}) # examplesIf

# a list of vectors
iris |>
  group_by(Species) |>
  group_map(~ quantile(.x$Petal.Length, probs = c(0.25, 0.5, 0.75)))

# to use group_modify() the lambda must return a data frame
iris |>
  group_by(Species) |>
  group_modify(~ {
     quantile(.x$Petal.Length, probs = c(0.25, 0.5, 0.75)) |>
     tibble::enframe(name = "prob", value = "quantile")
  })

iris |>
  group_by(Species) |>
  group_modify(~ {
    .x |>
      purrr::map_dfc(fivenum) |>
      mutate(nms = c("min", "Q1", "median", "Q3", "max"))
  })

# group_walk() is for side effects
dir.create(temp <- tempfile())
iris |>
  group_by(Species) |>
  group_walk(~ write.csv(.x, file = file.path(temp, paste0(.y$Species, ".csv"))))
list.files(temp, pattern = "csv$")
unlink(temp, recursive = TRUE)

# group_modify() and ungrouped data frames
mtcars |>
  group_modify(~ head(.x, 2L))