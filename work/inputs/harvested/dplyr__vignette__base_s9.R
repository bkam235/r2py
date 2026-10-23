# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
starwars |> filter(species == "Human")
starwars |> filter(mass > 1000)
starwars |> filter(hair_color == "none" & eye_color == "black")