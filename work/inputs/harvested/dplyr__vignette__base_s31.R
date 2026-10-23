# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
mtcars |>
  group_by(cyl) |>
  summarise(mean = mean(disp), n = n())