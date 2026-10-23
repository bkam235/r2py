# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_cols.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
gdf <- iris |> group_by(Species)
gdf |> select(group_cols())

# Remove the grouping variables from mutate selections:
gdf |> mutate_at(vars(-group_cols()), `/`, 100)
# -> No longer necessary with across()
gdf |> mutate(across(everything(), ~ . / 100))