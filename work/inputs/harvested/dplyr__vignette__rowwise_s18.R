# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
df <- tibble(g = 1:2, y = list(1:3, "a"))
gf <- df |> group_by(g)
rf <- df |> rowwise(g)