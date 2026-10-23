# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: cell-specification.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 20

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token() && rlang::is_interactive()) withAutoprint({ # examplesIf
ss <- gs4_example("mini-gap")

# Specify only the rows or only the columns
read_sheet(ss, range = cell_rows(1:3))
read_sheet(ss, range = cell_cols("C:D"))
read_sheet(ss, range = cell_cols(1))

# Specify upper or lower bound on row or column
read_sheet(ss, range = cell_rows(c(NA, 4)))
read_sheet(ss, range = cell_cols(c(NA, "D")))
read_sheet(ss, range = cell_rows(c(3, NA)))
read_sheet(ss, range = cell_cols(c(2, NA)))
read_sheet(ss, range = cell_cols(c("C", NA)))

# Specify a partially open rectangle
read_sheet(ss, range = cell_limits(c(2, 3), c(NA, NA)), col_names = FALSE)
read_sheet(ss, range = cell_limits(c(1, 2), c(NA, 4)))
}) # examplesIf