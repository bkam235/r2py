# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: oob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 15

suppressPackageStartupMessages(library(scales))
# Censoring replaces out of bounds values with NAs
oob_censor(c(-Inf, -1, 0.5, 1, 2, NA, Inf))
oob_censor_any(c(-Inf, -1, 0.5, 1, 2, NA, Inf))

# Squishing replaces out of bounds values with the nearest range limit
oob_squish(c(-Inf, -1, 0.5, 1, 2, NA, Inf))
oob_squish_any(c(-Inf, -1, 0.5, 1, 2, NA, Inf))
oob_squish_infinite(c(-Inf, -1, 0.5, 1, 2, NA, Inf))

# Keeping does not alter values
oob_keep(c(-Inf, -1, 0.5, 1, 2, NA, Inf))

# Discarding will remove out of bounds values
oob_discard(c(-Inf, -1, 0.5, 1, 2, NA, Inf))