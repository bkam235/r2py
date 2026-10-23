# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 8

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = c("a", "b"), y = c(1, 1), z = c(-1, 1))

# Find all rows where EVERY numeric variable is greater than zero
df |> filter(if_all(where(is.numeric), ~ .x > 0))

# Find all rows where ANY numeric variable is greater than zero
df |> filter(if_any(where(is.numeric), ~ .x > 0))