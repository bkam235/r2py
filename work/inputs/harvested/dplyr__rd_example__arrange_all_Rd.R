# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: arrange_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 9

suppressPackageStartupMessages(library(dplyr))
df <- as_tibble(mtcars)
arrange_all(df)
# ->
arrange(df, pick(everything()))

arrange_all(df, desc)
# ->
arrange(df, across(everything(), desc))