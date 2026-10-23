# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s27
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 7

suppressPackageStartupMessages(library(dplyr))
df <- tribble(
  ~ n, ~ min, ~ max,
    1,     0,     1,
    2,    10,   100,
    3,   100,  1000,
)