# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = 2, y = 4, z = 8)
df |> mutate_all(~ .x / y)

df |> mutate(across(everything(), ~ .x / y))