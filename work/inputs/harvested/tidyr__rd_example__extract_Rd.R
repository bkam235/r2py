# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: extract.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 14

suppressPackageStartupMessages(library(tidyr))
df <- tibble(x = c(NA, "a-b", "a-d", "b-c", "d-e"))
df |> extract(x, "A")
df |> extract(x, c("A", "B"), "([[:alnum:]]+)-([[:alnum:]]+)")

# Now recommended
df |>
  separate_wider_regex(
    x,
    patterns = c(A = "[[:alnum:]]+", "-", B = "[[:alnum:]]+")
  )

# If no match, NA:
df |> extract(x, c("A", "B"), "([a-d]+)-([a-d]+)")