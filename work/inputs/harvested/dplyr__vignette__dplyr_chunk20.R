# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_chunk20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.Rmd
# lines: 7

suppressPackageStartupMessages(library(dplyr))
a1 <- group_by(starwars, species, sex)
a2 <- select(a1, height, mass)
a3 <- summarise(a2,
  height = mean(height, na.rm = TRUE),
  mass = mean(mass, na.rm = TRUE)
)