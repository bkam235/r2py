# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 5

suppressPackageStartupMessages(library(vroom))
vroom(
  vroom_example("mtcars.csv"),
  col_types = list(hp = col_integer(), cyl = col_skip(), gear = col_factor())
)