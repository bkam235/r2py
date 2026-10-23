# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: bind_cols.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 7

suppressPackageStartupMessages(library(dplyr))
df1 <- tibble(x = 1:3)
df2 <- tibble(y = 3:1)
bind_cols(df1, df2)

# Row sizes must be compatible when column-binding
try(bind_cols(tibble(x = 1:3), tibble(y = 1:2)))