# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: pull.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 15

suppressPackageStartupMessages(library(dplyr))
mtcars |> pull(-1)
mtcars |> pull(1)
mtcars |> pull(cyl)
if (requireNamespace("dbplyr", quietly = TRUE) && requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf

# Also works for remote sources
df <- dbplyr::memdb_frame(x = 1:10, y = 10:1, .name = "pull-ex")
df |>
  mutate(z = x * y) |>
  pull()
}) # examplesIf

# Pull a named vector
starwars |> pull(height, name)