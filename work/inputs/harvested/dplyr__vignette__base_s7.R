# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 8

suppressPackageStartupMessages(library(dplyr))
df <- tibble(
  x = sample(10, 100, rep = TRUE),
  y = sample(10, 100, rep = TRUE)
)

df |> distinct(x) # selected columns
df |> distinct(x, .keep_all = TRUE) # whole data frame