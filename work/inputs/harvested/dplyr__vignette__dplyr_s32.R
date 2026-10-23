# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_s32
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
group_by(starwars, sex)
group_by(starwars, sex = as.factor(sex))
group_by(starwars, height_binned = cut(height, 3))