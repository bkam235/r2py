# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: spec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 6

suppressPackageStartupMessages(library(readr))
df <- read_csv(readr_example("mtcars.csv"))
s <- spec(df)
s

cols_condense(s)