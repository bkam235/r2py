# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: new_tibble.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 9

suppressPackageStartupMessages(library(tibble))
# The nrow argument can be omitted:
new_tibble(list(a = 1:3, b = 4:6))

# Existing row.names attributes are ignored:
try(validate_tibble(new_tibble(trees, nrow = 3)))

# The length of all columns must be compatible with the nrow argument:
try(validate_tibble(new_tibble(list(a = 1:3, b = 4:6), nrow = 2)))