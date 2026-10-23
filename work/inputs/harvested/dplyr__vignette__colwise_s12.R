# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = 1:3, y = 3:5, z = 5:7)
mult <- list(x = 1, y = 10, z = 100)

df |> mutate(across(all_of(names(mult)), ~ .x * mult[[cur_column()]]))