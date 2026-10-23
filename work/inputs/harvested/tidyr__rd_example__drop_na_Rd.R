# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: drop_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 7

suppressPackageStartupMessages(library(tidyr))
df <- tibble(x = c(1, 2, NA), y = c("a", NA, "b"))
df |> drop_na()
df |> drop_na(x)

vars <- "y"
df |> drop_na(x, any_of(vars))