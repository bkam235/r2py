# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: are_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 13

suppressPackageStartupMessages(library(rlang))
# are_na() is vectorised and works regardless of the type
are_na(c(1, 2, NA))
are_na(c(1L, NA, 3L))

# is_na() checks for scalar input and works for all types
is_na(NA)
is_na(na_dbl)
is_na(character(0))

# There are typed versions as well:
is_lgl_na(NA)
is_lgl_na(na_dbl)