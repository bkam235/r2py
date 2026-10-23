# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: tribble.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 27

suppressPackageStartupMessages(library(tibble))
tribble(
  ~colA, ~colB,
  "a",   1,
  "b",   2,
  "c",   3
)

# tribble will create a list column if the value in any cell is
# not a scalar
tribble(
  ~x,  ~y,
  "a", 1:3,
  "b", 4:6
)
if (rlang::is_installed("dplyr") && packageVersion("dplyr") >= "1.0.5") withAutoprint({ # examplesIf

# Use dplyr::mutate(dplyr::across(...)) to assign an explicit type
tribble(
  ~a, ~b, ~c,
  1, "2000-01-01", "1.5"
) %>%
  dplyr::mutate(
    dplyr::across(a, as.integer),
    dplyr::across(b, as.Date)
  )
}) # examplesIf