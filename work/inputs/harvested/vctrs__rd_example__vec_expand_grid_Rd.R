# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_expand_grid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 11

suppressPackageStartupMessages(library(vctrs))
vec_expand_grid(x = 1:2, y = 1:3)

# Use `.vary` to match `expand.grid()`:
vec_expand_grid(x = 1:2, y = 1:3, .vary = "fastest")

# Can also expand data frames
vec_expand_grid(
  x = data_frame(a = 1:2, b = 3:4),
  y = 1:4
)