# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: select_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 33

suppressPackageStartupMessages(library(dplyr))
mtcars <- as_tibble(mtcars) # for nicer printing

mtcars |> rename_all(toupper)
# ->
mtcars |> rename_with(toupper)

# NB: the transformation comes first in rename_with
is_whole <- function(x) all(floor(x) == x)
mtcars |> rename_if(is_whole, toupper)
# ->
mtcars |> rename_with(toupper, where(is_whole))

mtcars |> rename_at(vars(mpg:hp), toupper)
# ->
mtcars |> rename_with(toupper, mpg:hp)

# You now must select() and then rename

mtcars |> select_all(toupper)
# ->
mtcars |> rename_with(toupper)

# Selection drops unselected variables:
mtcars |> select_if(is_whole, toupper)
# ->
mtcars |> select(where(is_whole)) |> rename_with(toupper)

mtcars |> select_at(vars(-contains("ar"), starts_with("c")), toupper)
# ->
mtcars |>
  select(!contains("ar") | starts_with("c")) |>
  rename_with(toupper)