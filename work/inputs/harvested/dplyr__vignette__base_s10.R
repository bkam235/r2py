# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
subset(starwars, species == "Human")
subset(starwars, mass > 1000)
subset(starwars, hair_color == "none" & eye_color == "black")