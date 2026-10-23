# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
summarise(
  select(
    group_by(starwars, species, sex),
    height, mass
  ),
  height = mean(height, na.rm = TRUE),
  mass = mean(mass, na.rm = TRUE)
)