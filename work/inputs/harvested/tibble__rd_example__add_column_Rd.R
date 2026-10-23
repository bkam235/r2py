# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: add_column.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 12

suppressPackageStartupMessages(library(tibble))
# add_column ---------------------------------
df <- tibble(x = 1:3, y = 3:1)

df %>% add_column(z = -1:1, w = 0)
df %>% add_column(z = -1:1, .before = "y")

# You can't overwrite existing columns
try(df %>% add_column(x = 4:6))

# You can't create new observations
try(df %>% add_column(z = 1:5))