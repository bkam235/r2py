# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
# to front
mtcars |> relocate(gear, carb)

# to back
mtcars |> relocate(mpg, cyl, .after = last_col())