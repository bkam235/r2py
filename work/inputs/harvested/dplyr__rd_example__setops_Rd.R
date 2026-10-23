# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: setops.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 22

suppressPackageStartupMessages(library(dplyr))
df1 <- tibble(x = 1:3)
df2 <- tibble(x = 3:5)

intersect(df1, df2)
union(df1, df2)
union_all(df1, df2)
setdiff(df1, df2)
setdiff(df2, df1)
symdiff(df1, df2)

setequal(df1, df2)
setequal(df1, df1[3:1, ])

# Note that the following functions remove pre-existing duplicates:
df1 <- tibble(x = c(1:3, 3, 3))
df2 <- tibble(x = c(3:5, 5))

intersect(df1, df2)
union(df1, df2)
setdiff(df1, df2)
symdiff(df1, df2)