# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: layout_column_wrap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 18

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
x <- card("A simple card")

# Always has 2 columns (on non-mobile)
layout_column_wrap(width = 1/2, x, x, x)

# Automatically lays out three cards into columns
# such that each column is at least 200px wide:
layout_column_wrap(x, x, x)

# To use larger column widths by default, set `width`.
# This example has 3 columns when the screen is at least 900px wide:
layout_column_wrap(width = "300px", x, x, x)

# You can add a list of items, spliced with rlang's `!!!` operator
layout_column_wrap(!!!list(x, x, x))
}) # examplesIf