# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: glimpse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 10

suppressPackageStartupMessages(library(dplyr))
glimpse(mtcars)

# Note that original x is (invisibly) returned, allowing `glimpse()` to be
# used within a pipeline.
mtcars |>
  glimpse() |>
  select(1:3)

glimpse(starwars)