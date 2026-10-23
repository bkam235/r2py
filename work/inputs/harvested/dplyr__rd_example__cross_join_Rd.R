# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: cross_join.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
# Cross joins match each row in `x` to every row in `y`.
# Data within the columns is not used in the matching process.
cross_join(band_instruments, band_members)

# Control the suffix added to variables duplicated in
# `x` and `y` with `suffix`.
cross_join(band_instruments, band_members, suffix = c("", "_y"))