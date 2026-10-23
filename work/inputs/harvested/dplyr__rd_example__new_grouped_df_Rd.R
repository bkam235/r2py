# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: new_grouped_df.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
# 5 bootstrap samples
tbl <- new_grouped_df(
  tibble(x = rnorm(10)),
  groups = tibble(".rows" := replicate(5, sample(1:10, replace = TRUE), simplify = FALSE))
)
# mean of each bootstrap sample
summarise(tbl, x = mean(x))