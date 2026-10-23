# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: bind_rows.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 14

suppressPackageStartupMessages(library(dplyr))
df1 <- tibble(x = 1:2, y = letters[1:2])
df2 <- tibble(x = 4:5, z = 1:2)

# You can supply individual data frames as arguments:
bind_rows(df1, df2)

# Or a list of data frames:
bind_rows(list(df1, df2))

# When you supply a column name with the `.id` argument, a new
# column is created to link each row to its original data frame
bind_rows(list(df1, df2), .id = "id")
bind_rows(list(a = df1, b = df2), .id = "id")