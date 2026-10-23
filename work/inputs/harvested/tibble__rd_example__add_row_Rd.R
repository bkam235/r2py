# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: add_row.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 22

suppressPackageStartupMessages(library(tibble))
# add_row ---------------------------------
df <- tibble(x = 1:3, y = 3:1)

df %>% add_row(x = 4, y = 0)

# You can specify where to add the new rows
df %>% add_row(x = 4, y = 0, .before = 2)

# You can supply vectors, to add multiple rows (this isn't
# recommended because it's a bit hard to read)
df %>% add_row(x = 4:5, y = 0:-1)

# Use tibble_row() to add one row only
df %>% add_row(tibble_row(x = 4, y = 0))
try(df %>% add_row(tibble_row(x = 4:5, y = 0:-1)))

# Absent variables get missing values
df %>% add_row(x = 4)

# You can't create new variables
try(df %>% add_row(z = 10))