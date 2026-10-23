# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
try({
gf |> mutate(y2 = y)
rf |> mutate(y2 = y)
rf |> mutate(y2 = list(y))
})