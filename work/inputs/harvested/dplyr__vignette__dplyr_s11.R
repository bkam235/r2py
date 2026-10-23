# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
# Select columns by name
starwars |> select(hair_color, skin_color, eye_color)
# Select all columns between hair_color and eye_color (inclusive)
starwars |> select(hair_color:eye_color)
# Select all columns except those from hair_color to eye_color (inclusive)
starwars |> select(!(hair_color:eye_color))
# Select all columns ending with color
starwars |> select(ends_with("color"))