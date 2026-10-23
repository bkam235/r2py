# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_nest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 16

suppressPackageStartupMessages(library(dplyr))
#----- use case 1: a grouped data frame
iris |>
  group_by(Species) |>
  group_nest()

# this can be useful if the grouped data has been altered before nesting
iris |>
  group_by(Species) |>
  filter(Sepal.Length > mean(Sepal.Length)) |>
  group_nest()

#----- use case 2: using group_nest() on a ungrouped data frame with
#                  a grouping specification that uses the data mask
starwars |>
  group_nest(species, homeworld)