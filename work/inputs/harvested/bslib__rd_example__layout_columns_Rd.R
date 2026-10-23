# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: layout_columns.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 40

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
x <- card("A simple card")

page_fillable(
  layout_columns(x, x, x, x)
)

# Or add a list of items, spliced with rlang's `!!!` operator
page_fillable(
 layout_columns(!!!list(x, x, x))
)

page_fillable(
  layout_columns(
    col_widths = c(6, 6, 12),
    x, x, x
  )
)

page_fillable(
  layout_columns(
    col_widths = c(6, 6, -2, 8),
    row_heights = c(1, 3),
    x, x, x
  )
)

page_fillable(
  fillable_mobile = TRUE,
  layout_columns(
    col_widths = breakpoints(
      sm = c(12, 12, 12),
      md = c(6, 6, 12),
      lg = c(4, 4, 4)
    ),
    x, x, x
  )
)
}) # examplesIf