# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
df <- data.frame(x = c(1, 2, 3), y = c(1, 4, 9))

df |>
  summarise(n = n(), across(where(is.numeric), sd))