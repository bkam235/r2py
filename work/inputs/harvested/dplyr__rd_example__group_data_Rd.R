# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_data.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 12

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = c(1,1,2,2))
group_vars(df)
group_rows(df)
group_data(df)
group_indices(df)

gf <- group_by(df, x)
group_vars(gf)
group_rows(gf)
group_data(gf)
group_indices(gf)