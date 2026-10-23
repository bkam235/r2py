# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: grouping_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\grouping.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
bmi_breaks <- c(0, 18.5, 25, 30, Inf)

starwars |>
  group_by(bmi_cat = cut(mass/(height/100)^2, breaks=bmi_breaks)) |>
  tally()