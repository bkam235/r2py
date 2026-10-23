# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: two-table_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\two-table.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
df1 <- tibble(x = c(1, 1, 2), y = 1:3)
df2 <- tibble(x = c(1, 1, 2), z = c("a", "b", "a"))

df1 |> left_join(df2)