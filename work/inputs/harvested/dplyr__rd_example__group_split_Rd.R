# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_split.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 5

suppressPackageStartupMessages(library(dplyr))
ir <- iris |> group_by(Species)

group_split(ir)
group_keys(ir)