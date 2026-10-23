# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: to_string.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 31

suppressPackageStartupMessages(library(cellranger))
## exactly one ra_ref --> string
to_string(ra_ref())
to_string(ra_ref(), fo = "A1")
to_string(ra_ref(), fo = "A1", strict = FALSE)
to_string(ra_ref(row_ref = 3, col_ref = 2))
to_string(ra_ref(row_ref = 3, col_ref = 2, sheet = "helloooo"))
(mixed_ref <- ra_ref(row_ref = 10, row_abs = FALSE, col_ref = 3))
to_string(mixed_ref)

## this will raise warning and generate NA, because row reference is
## relative and format is A1
to_string(mixed_ref, fo = "A1")

## a list of ra_ref's --> character vector
ra_ref_list <-
  list(ra_ref(), ra_ref(2, TRUE, 5, TRUE), ra_ref(2, FALSE, 5, TRUE))
to_string_v(ra_ref_list)

## cell_addr --> string
(ca <- cell_addr(3, 8))
to_string(ca)
to_string(ca, fo = "A1")

(ca <- cell_addr(1:4, 3))
to_string(ca)
to_string(ca, fo = "A1")
## explicitly go from cell_addr, length > 1 --> character vector
(ca <- cell_addr(1:4, 3))
to_string_v(ca)
to_string_v(ca, fo = "A1")