# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: filter-joins.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
# "Filtering" joins keep cases from the LHS
band_members |> semi_join(band_instruments)
band_members |> anti_join(band_instruments)

# To suppress the message about joining variables, supply `by`
band_members |> semi_join(band_instruments, by = join_by(name))
# This is good practice in production code