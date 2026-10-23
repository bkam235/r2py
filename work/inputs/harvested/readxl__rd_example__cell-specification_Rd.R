# r2py crawler metadata
# package: readxl
# source_type: rd_example
# topic: cell-specification.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\help
# lines: 41

suppressPackageStartupMessages(library(readxl))
path <- readxl_example("geometry.xls")
## Rows 1 and 2 are empty (as are rows 7 and higher)
## Column 1 aka "A" is empty (as are columns 5 of "E" and higher)

# By default, the populated data cells are "shrink-wrapped" into a
# minimal data frame
read_excel(path)

# Specific rectangle that is subset of populated cells, possibly improper
read_excel(path, range = "B3:D6")
read_excel(path, range = "C3:D5")

# Specific rectangle that forces inclusion of unpopulated cells
read_excel(path, range = "A3:D5")
read_excel(path, range = "A4:E5")
read_excel(path, range = "C5:E7")

# Anchor a rectangle of specified size at a particular cell
read_excel(path, range = anchored("C4", dim = c(3, 2)), col_names = FALSE)

# Specify only the rows
read_excel(path, range = cell_rows(3:5))
## is equivalent to
read_excel(path, range = cell_rows(c(3, 5)))

# Specify only the columns by column number or letter
read_excel(path, range = cell_cols("C:D"))
read_excel(path, range = cell_cols(2))

# Specify exactly one row or column bound
read_excel(path, range = cell_rows(c(5, NA)))
read_excel(path, range = cell_rows(c(NA, 4)))
read_excel(path, range = cell_cols(c("C", NA)))
read_excel(path, range = cell_cols(c(NA, 2)))

# General open rectangles
# upper left = C4, everything else unspecified
read_excel(path, range = cell_limits(c(4, 3), c(NA, NA)))
# upper right = D4, everything else unspecified
read_excel(path, range = cell_limits(c(4, NA), c(NA, 4)))