# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: output_column.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 4

suppressPackageStartupMessages(library(readr))
# Most columns are not altered, but POSIXct are converted to ISO8601.
x <- parse_datetime("2016-01-01")
str(output_column(x))