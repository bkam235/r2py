# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: nest_join.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 7

suppressPackageStartupMessages(library(dplyr))
df1 <- tibble(x = 1:3)
df2 <- tibble(x = c(2, 3, 3), y = c("a", "b", "c"))

out <- nest_join(df1, df2)
out
out$df2