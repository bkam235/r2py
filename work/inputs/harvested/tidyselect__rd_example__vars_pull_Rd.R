# r2py crawler metadata
# package: tidyselect
# source_type: rd_example
# topic: vars_pull.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\help
# lines: 10

suppressPackageStartupMessages(library(tidyselect))
# It takes its argument by expression:
vars_pull(letters, c)

# Negative numbers select from the end:
vars_pull(letters, -3)

# You can unquote variables:
var <- 10
vars_pull(letters, !!var)